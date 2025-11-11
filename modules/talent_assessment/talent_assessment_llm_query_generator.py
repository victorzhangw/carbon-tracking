"""
人才評鑑系統 LLM SQL 查詢生成器
使用 LLM 理解使用者意圖並生成對應的 SQL 查詢
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from modules.talent_assessment.talent_assessment_query_validator import TalentAssessmentQueryValidator


class TalentAssessmentLLMQueryGenerator:
    """使用 LLM 生成 SQL 查詢的類別"""
    
    def __init__(self, api_key: str, base_url: str = None, model: str = "deepseek-ai/DeepSeek-V3"):
        """
        初始化 LLM 查詢生成器
        
        Args:
            api_key: API 金鑰
            base_url: API 基礎 URL（可選）
            model: 使用的模型名稱
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
        self.model = model
        self.validator = TalentAssessmentQueryValidator()
        
        # 建立資料庫結構的描述
        self.db_schema_description = self._build_schema_description()
    
    def _build_schema_description(self) -> str:
        """建立資料庫結構的文字描述"""
        schema_desc = "# 人才評鑑系統資料庫結構\n\n"
        
        tables = self.validator.get_all_tables()
        
        for table_name, table_info in tables.items():
            schema_desc += f"## 表格: {table_name}\n"
            schema_desc += f"欄位: {', '.join(table_info['columns'])}\n"
            schema_desc += f"主鍵: {table_info['primary_key']}\n"
            
            if 'foreign_keys' in table_info:
                schema_desc += "外鍵關聯:\n"
                for fk_col, ref in table_info['foreign_keys'].items():
                    schema_desc += f"  - {fk_col} -> {ref}\n"
            
            schema_desc += "\n"
        
        return schema_desc
    
    def generate_sql_from_intent(self, user_intent: str, context: Dict = None) -> Dict:
        """
        根據使用者意圖生成 SQL 查詢
        
        Args:
            user_intent: 使用者的查詢意圖（自然語言）
            context: 額外的上下文資訊（如已知的參數值）
        
        Returns:
            包含生成的 SQL、參數、說明等資訊的字典
        """
        # 先檢查是否有預定義的模板可以使用
        suggestions = self.validator.suggest_query_for_intent(user_intent)
        
        # 建立 LLM 提示
        system_prompt = f"""你是一個專業的 SQL 查詢生成助手，專門為人才評鑑系統生成 PostgreSQL 查詢。

{self.db_schema_description}

## 重要規則：
1. 只生成 SELECT 查詢，不允許 INSERT、UPDATE、DELETE、DROP 等操作
2. 使用 PostgreSQL 語法
3. 使用參數化查詢，參數用 %s 表示
4. JOIN 時必須使用正確的外鍵關聯
5. 中文欄位別名使用 AS 關鍵字
6. 使用 STRING_AGG 而不是 GROUP_CONCAT（PostgreSQL 語法）
7. 確保所有表格和欄位名稱都存在於資料庫結構中

## 輸出格式：
請以 JSON 格式回應，包含以下欄位：
{{
    "sql": "生成的 SQL 查詢",
    "params": ["參數列表"],
    "param_descriptions": {{"param1": "參數1的描述"}},
    "explanation": "查詢的說明",
    "tables_used": ["使用的表格列表"]
}}
"""
        
        user_prompt = f"""使用者查詢意圖：{user_intent}

"""
        
        if context:
            user_prompt += f"已知上下文資訊：{json.dumps(context, ensure_ascii=False)}\n\n"
        
        if suggestions:
            user_prompt += "參考查詢模板：\n"
            for i, suggestion in enumerate(suggestions, 1):
                user_prompt += f"\n模板 {i}: {suggestion['description']}\n"
                user_prompt += f"```sql\n{suggestion['query']}\n```\n"
        
        user_prompt += "\n請根據使用者意圖生成對應的 SQL 查詢。"
        
        try:
            # 呼叫 LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # 降低溫度以獲得更確定的結果
                max_tokens=2000
            )
            
            # 解析回應
            content = response.choices[0].message.content
            
            # 嘗試提取 JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # 如果沒有找到 JSON，嘗試提取 SQL
                sql_match = re.search(r'```sql\n(.*?)\n```', content, re.DOTALL)
                if sql_match:
                    result = {
                        "sql": sql_match.group(1).strip(),
                        "params": [],
                        "param_descriptions": {},
                        "explanation": "LLM 生成的查詢",
                        "tables_used": []
                    }
                else:
                    raise ValueError("無法從 LLM 回應中提取 SQL 查詢")
            
            # 驗證生成的 SQL
            is_valid, errors = self.validator.validate_query(result['sql'])
            
            result['is_valid'] = is_valid
            result['validation_errors'] = errors
            
            if not is_valid:
                result['warning'] = "生成的查詢未通過驗證，請檢查錯誤訊息"
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "sql": None,
                "is_valid": False
            }
    
    def explain_query(self, sql_query: str) -> str:
        """
        使用 LLM 解釋 SQL 查詢的含義
        
        Args:
            sql_query: 要解釋的 SQL 查詢
        
        Returns:
            查詢的自然語言解釋
        """
        system_prompt = """你是一個 SQL 查詢解釋專家。請用清晰、易懂的中文解釋 SQL 查詢的含義。

解釋應包含：
1. 查詢的目的
2. 涉及的表格和關聯
3. 篩選條件
4. 返回的資料內容
"""
        
        user_prompt = f"請解釋以下 SQL 查詢：\n\n```sql\n{sql_query}\n```"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"解釋查詢時發生錯誤：{str(e)}"
    
    def optimize_query(self, sql_query: str) -> Dict:
        """
        使用 LLM 優化 SQL 查詢
        
        Args:
            sql_query: 要優化的 SQL 查詢
        
        Returns:
            包含優化建議的字典
        """
        system_prompt = f"""你是一個 PostgreSQL 查詢優化專家。請分析並優化給定的 SQL 查詢。

{self.db_schema_description}

請提供：
1. 優化後的 SQL 查詢
2. 優化的理由
3. 效能改進建議
4. 索引建議

以 JSON 格式回應：
{{
    "optimized_sql": "優化後的 SQL",
    "improvements": ["改進點列表"],
    "index_suggestions": ["索引建議"],
    "explanation": "優化說明"
}}
"""
        
        user_prompt = f"請優化以下 SQL 查詢：\n\n```sql\n{sql_query}\n```"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # 嘗試提取 JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "error": "無法解析優化建議",
                    "raw_response": content
                }
            
        except Exception as e:
            return {
                "error": str(e)
            }


# 使用範例
if __name__ == "__main__":
    # 注意：需要設定你的 API 金鑰
    API_KEY = "your-api-key-here"
    BASE_URL = "https://api.siliconflow.cn"
    
    generator = TalentAssessmentLLMQueryGenerator(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    
    print("=== 人才評鑑系統 LLM SQL 查詢生成器 ===\n")
    
    # 測試案例
    test_intents = [
        "查詢 Howard 的所有特質分數",
        "找出品格誠信素養分數最高的前 10 名受測者",
        "查詢所有同理心分數低於 50 的受測者",
        "顯示專案經理職位的受測者的向度分數分布",
        "查詢 2025 年 9 月完成評鑑的所有受測者"
    ]
    
    for i, intent in enumerate(test_intents, 1):
        print(f"\n{'='*60}")
        print(f"測試 {i}: {intent}")
        print('='*60)
        
        result = generator.generate_sql_from_intent(intent)
        
        if 'error' in result:
            print(f"❌ 錯誤: {result['error']}")
        else:
            print(f"\n✅ 生成的 SQL:")
            print(result['sql'])
            
            if result.get('params'):
                print(f"\n📝 參數: {result['params']}")
            
            if result.get('explanation'):
                print(f"\n💡 說明: {result['explanation']}")
            
            if not result['is_valid']:
                print(f"\n⚠️  驗證錯誤:")
                for error in result['validation_errors']:
                    print(f"  - {error}")
