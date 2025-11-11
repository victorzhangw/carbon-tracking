"""
人才評鑑系統 SQL 查詢驗證器
根據資料庫設計文件驗證和生成 SQL 查詢
"""

import re
from typing import Dict, List, Tuple, Optional

class TalentAssessmentQueryValidator:
    """人才評鑑系統 SQL 查詢驗證器"""
    
    def __init__(self):
        # 定義資料庫結構
        self.tables = {
            'test_takers': {
                'columns': ['id', 'name', 'email', 'job_role', 'identity_type', 'created_at', 'updated_at'],
                'primary_key': 'id',
                'unique': ['email']
            },
            'assessment_items': {
                'columns': ['id', 'code', 'name_zh', 'name_en', 'description', 'is_active', 'created_at'],
                'primary_key': 'id',
                'unique': ['code']
            },
            'assessment_records': {
                'columns': ['id', 'test_taker_id', 'assessment_item_id', 'invited_at', 'completed_at', 'status', 'created_at'],
                'primary_key': 'id',
                'foreign_keys': {
                    'test_taker_id': 'test_takers.id',
                    'assessment_item_id': 'assessment_items.id'
                }
            },
            'trait_definitions': {
                'columns': ['id', 'code', 'name_zh', 'name_en', 'high_score_desc', 'low_score_desc', 'additional_info', 'category', 'created_at'],
                'primary_key': 'id',
                'unique': ['code']
            },
            'trait_scores': {
                'columns': ['id', 'assessment_record_id', 'trait_id', 'score', 'created_at'],
                'primary_key': 'id',
                'foreign_keys': {
                    'assessment_record_id': 'assessment_records.id',
                    'trait_id': 'trait_definitions.id'
                }
            },
            'dimension_definitions': {
                'columns': ['id', 'code', 'name_zh', 'name_en', 'description', 'display_order', 'created_at'],
                'primary_key': 'id',
                'unique': ['code']
            },
            'dimension_scores': {
                'columns': ['id', 'assessment_record_id', 'dimension_id', 'score', 'created_at'],
                'primary_key': 'id',
                'foreign_keys': {
                    'assessment_record_id': 'assessment_records.id',
                    'dimension_id': 'dimension_definitions.id'
                }
            },
            'trait_dimension_mapping': {
                'columns': ['id', 'trait_id', 'dimension_id', 'weight', 'created_at'],
                'primary_key': 'id',
                'foreign_keys': {
                    'trait_id': 'trait_definitions.id',
                    'dimension_id': 'dimension_definitions.id'
                }
            },
            'tag_definitions': {
                'columns': ['id', 'code', 'name_zh', 'tag_type', 'created_at'],
                'primary_key': 'id',
                'unique': ['code']
            },
            'dimension_tags': {
                'columns': ['id', 'assessment_record_id', 'dimension_id', 'tag_id', 'created_at'],
                'primary_key': 'id',
                'foreign_keys': {
                    'assessment_record_id': 'assessment_records.id',
                    'dimension_id': 'dimension_definitions.id',
                    'tag_id': 'tag_definitions.id'
                }
            },
            'interview_questions': {
                'columns': ['id', 'dimension_id', 'question_text', 'question_type', 'display_order', 'created_at'],
                'primary_key': 'id',
                'foreign_keys': {
                    'dimension_id': 'dimension_definitions.id'
                }
            },
            'comprehensive_analysis': {
                'columns': ['id', 'assessment_record_id', 'strength_dimension_id', 'strength_description', 
                           'weakness_dimension_id', 'weakness_description', 'created_at'],
                'primary_key': 'id',
                'foreign_keys': {
                    'assessment_record_id': 'assessment_records.id',
                    'strength_dimension_id': 'dimension_definitions.id',
                    'weakness_dimension_id': 'dimension_definitions.id'
                }
            }
        }
        
        # 常見的查詢模板
        self.query_templates = {
            'get_test_taker_report': """
                SELECT 
                    tt.name AS 受測者姓名,
                    tt.email AS 電子信箱,
                    tt.job_role AS 職務角色,
                    ai.name_zh AS 測驗項目,
                    ar.invited_at AS 邀請時間,
                    ar.completed_at AS 結果取得時間
                FROM assessment_records ar
                JOIN test_takers tt ON ar.test_taker_id = tt.id
                JOIN assessment_items ai ON ar.assessment_item_id = ai.id
                WHERE tt.email = %s
            """,
            'get_trait_scores': """
                SELECT 
                    td.name_zh AS 特質名稱,
                    ts.score AS 分數,
                    td.high_score_desc AS 高分描述,
                    td.low_score_desc AS 低分描述
                FROM trait_scores ts
                JOIN trait_definitions td ON ts.trait_id = td.id
                JOIN assessment_records ar ON ts.assessment_record_id = ar.id
                JOIN test_takers tt ON ar.test_taker_id = tt.id
                WHERE tt.email = %s
                ORDER BY ts.score DESC
            """,
            'get_dimension_scores': """
                SELECT 
                    dd.name_zh AS 向度名稱,
                    ds.score AS 分數,
                    dd.description AS 說明,
                    RANK() OVER (PARTITION BY ds.assessment_record_id ORDER BY ds.score DESC) AS 排名
                FROM dimension_scores ds
                JOIN dimension_definitions dd ON ds.dimension_id = dd.id
                JOIN assessment_records ar ON ds.assessment_record_id = ar.id
                JOIN test_takers tt ON ar.test_taker_id = tt.id
                WHERE tt.email = %s
                ORDER BY ds.score DESC
            """,
            'get_dimension_tags': """
                SELECT 
                    dd.name_zh AS 向度名稱,
                    STRING_AGG(tg.name_zh, ', ') AS 標籤列表
                FROM dimension_tags dt
                JOIN dimension_definitions dd ON dt.dimension_id = dd.id
                JOIN tag_definitions tg ON dt.tag_id = tg.id
                JOIN assessment_records ar ON dt.assessment_record_id = ar.id
                JOIN test_takers tt ON ar.test_taker_id = tt.id
                WHERE tt.email = %s AND tg.tag_type = %s
                GROUP BY dd.name_zh
            """,
            'get_interview_questions': """
                SELECT 
                    dd.name_zh AS 向度名稱,
                    iq.question_text AS 面試問題,
                    iq.question_type AS 問題類型
                FROM interview_questions iq
                JOIN dimension_definitions dd ON iq.dimension_id = dd.id
                WHERE dd.code = %s
                ORDER BY iq.display_order
            """,
            'get_comprehensive_analysis': """
                SELECT 
                    tt.name AS 受測者姓名,
                    sd.name_zh AS 優勢向度,
                    ca.strength_description AS 優勢描述,
                    wd.name_zh AS 劣勢向度,
                    ca.weakness_description AS 劣勢描述
                FROM comprehensive_analysis ca
                JOIN assessment_records ar ON ca.assessment_record_id = ar.id
                JOIN test_takers tt ON ar.test_taker_id = tt.id
                LEFT JOIN dimension_definitions sd ON ca.strength_dimension_id = sd.id
                LEFT JOIN dimension_definitions wd ON ca.weakness_dimension_id = wd.id
                WHERE tt.email = %s
            """
        }
    
    def validate_table_name(self, table_name: str) -> Tuple[bool, Optional[str]]:
        """驗證表格名稱是否存在"""
        if table_name not in self.tables:
            return False, f"表格 '{table_name}' 不存在於資料庫設計中"
        return True, None
    
    def validate_column_name(self, table_name: str, column_name: str) -> Tuple[bool, Optional[str]]:
        """驗證欄位名稱是否存在於指定表格"""
        if table_name not in self.tables:
            return False, f"表格 '{table_name}' 不存在"
        
        if column_name not in self.tables[table_name]['columns']:
            return False, f"欄位 '{column_name}' 不存在於表格 '{table_name}' 中"
        
        return True, None

    def validate_join(self, from_table: str, to_table: str, join_column: str) -> Tuple[bool, Optional[str]]:
        """驗證 JOIN 關聯是否正確"""
        if from_table not in self.tables:
            return False, f"來源表格 '{from_table}' 不存在"
        
        if to_table not in self.tables:
            return False, f"目標表格 '{to_table}' 不存在"
        
        # 檢查是否有外鍵關聯
        if 'foreign_keys' in self.tables[from_table]:
            fk = self.tables[from_table]['foreign_keys']
            if join_column in fk:
                expected_ref = fk[join_column]
                if expected_ref == f"{to_table}.{self.tables[to_table]['primary_key']}":
                    return True, None
                else:
                    return False, f"JOIN 關聯錯誤：{join_column} 應該關聯到 {expected_ref}"
        
        return False, f"表格 '{from_table}' 沒有到 '{to_table}' 的外鍵關聯"
    
    def extract_tables_from_query(self, query: str) -> List[str]:
        """從 SQL 查詢中提取表格名稱"""
        # 移除註解
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        
        # 提取 FROM 和 JOIN 後的表格名稱
        pattern = r'(?:FROM|JOIN)\s+(\w+)'
        matches = re.findall(pattern, query, re.IGNORECASE)
        
        return list(set(matches))
    
    def extract_columns_from_query(self, query: str) -> List[Tuple[str, str]]:
        """從 SQL 查詢中提取欄位名稱（表格.欄位）"""
        # 移除註解
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        
        # 提取 table.column 格式的欄位
        pattern = r'(\w+)\.(\w+)'
        matches = re.findall(pattern, query)
        
        return matches
    
    def validate_query(self, query: str) -> Tuple[bool, List[str]]:
        """驗證 SQL 查詢的正確性"""
        errors = []
        
        # 檢查是否為 SELECT 查詢
        if not re.search(r'^\s*SELECT', query, re.IGNORECASE):
            errors.append("只允許 SELECT 查詢")
            return False, errors
        
        # 檢查是否包含危險操作
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        for keyword in dangerous_keywords:
            if re.search(rf'\b{keyword}\b', query, re.IGNORECASE):
                errors.append(f"不允許使用 {keyword} 操作")
        
        if errors:
            return False, errors
        
        # 提取並驗證表格名稱
        tables = self.extract_tables_from_query(query)
        for table in tables:
            is_valid, error = self.validate_table_name(table)
            if not is_valid:
                errors.append(error)
        
        # 提取並驗證欄位名稱
        columns = self.extract_columns_from_query(query)
        for table, column in columns:
            is_valid, error = self.validate_column_name(table, column)
            if not is_valid:
                errors.append(error)
        
        if errors:
            return False, errors
        
        return True, []
    
    def get_query_template(self, template_name: str, params: List = None) -> Optional[str]:
        """獲取預定義的查詢模板"""
        if template_name not in self.query_templates:
            return None
        
        query = self.query_templates[template_name]
        
        # 如果提供了參數，進行格式化（僅用於展示，實際執行時應使用參數化查詢）
        if params:
            # 注意：這裡只是示例，實際應該使用參數化查詢
            return query
        
        return query
    
    def suggest_query_for_intent(self, user_intent: str) -> Optional[Dict]:
        """根據使用者意圖建議查詢"""
        intent_lower = user_intent.lower()
        
        suggestions = []
        
        if '受測者' in user_intent or '報告' in user_intent or '基本資料' in user_intent:
            suggestions.append({
                'template': 'get_test_taker_report',
                'description': '查詢受測者的完整評鑑報告',
                'required_params': ['email'],
                'query': self.query_templates['get_test_taker_report']
            })
        
        if '特質' in user_intent or '分數' in user_intent:
            suggestions.append({
                'template': 'get_trait_scores',
                'description': '查詢受測者的所有特質分數',
                'required_params': ['email'],
                'query': self.query_templates['get_trait_scores']
            })
        
        if '向度' in user_intent:
            suggestions.append({
                'template': 'get_dimension_scores',
                'description': '查詢受測者的向度分數與排名',
                'required_params': ['email'],
                'query': self.query_templates['get_dimension_scores']
            })
        
        if '標籤' in user_intent or '優勢' in user_intent or '劣勢' in user_intent:
            suggestions.append({
                'template': 'get_dimension_tags',
                'description': '查詢向度的標籤',
                'required_params': ['email', 'tag_type'],
                'query': self.query_templates['get_dimension_tags']
            })
        
        if '面試' in user_intent or '問題' in user_intent:
            suggestions.append({
                'template': 'get_interview_questions',
                'description': '查詢針對特定向度的面試問題',
                'required_params': ['dimension_code'],
                'query': self.query_templates['get_interview_questions']
            })
        
        if '綜合分析' in user_intent or '分析結果' in user_intent:
            suggestions.append({
                'template': 'get_comprehensive_analysis',
                'description': '查詢綜合分析結果',
                'required_params': ['email'],
                'query': self.query_templates['get_comprehensive_analysis']
            })
        
        return suggestions if suggestions else None
    
    def get_all_tables(self) -> Dict:
        """獲取所有表格資訊"""
        return self.tables
    
    def get_table_schema(self, table_name: str) -> Optional[Dict]:
        """獲取指定表格的結構"""
        return self.tables.get(table_name)


# 使用範例
if __name__ == "__main__":
    validator = TalentAssessmentQueryValidator()
    
    print("=== 人才評鑑系統 SQL 查詢驗證器 ===\n")
    
    # 測試 1: 驗證正確的查詢
    print("測試 1: 驗證正確的查詢")
    correct_query = """
        SELECT tt.name, tt.email, ar.completed_at
        FROM assessment_records ar
        JOIN test_takers tt ON ar.test_taker_id = tt.id
        WHERE tt.email = 'test@example.com'
    """
    is_valid, errors = validator.validate_query(correct_query)
    print(f"查詢有效: {is_valid}")
    if errors:
        print(f"錯誤: {errors}")
    print()
    
    # 測試 2: 驗證錯誤的表格名稱
    print("測試 2: 驗證錯誤的表格名稱")
    wrong_table_query = """
        SELECT * FROM wrong_table WHERE id = 1
    """
    is_valid, errors = validator.validate_query(wrong_table_query)
    print(f"查詢有效: {is_valid}")
    if errors:
        print(f"錯誤: {errors}")
    print()
    
    # 測試 3: 驗證危險操作
    print("測試 3: 驗證危險操作")
    dangerous_query = """
        DELETE FROM test_takers WHERE id = 1
    """
    is_valid, errors = validator.validate_query(dangerous_query)
    print(f"查詢有效: {is_valid}")
    if errors:
        print(f"錯誤: {errors}")
    print()
    
    # 測試 4: 根據意圖建議查詢
    print("測試 4: 根據意圖建議查詢")
    user_intent = "我想查詢受測者的特質分數"
    suggestions = validator.suggest_query_for_intent(user_intent)
    if suggestions:
        print(f"找到 {len(suggestions)} 個建議:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n建議 {i}:")
            print(f"  模板: {suggestion['template']}")
            print(f"  描述: {suggestion['description']}")
            print(f"  必要參數: {suggestion['required_params']}")
    print()
    
    # 測試 5: 獲取查詢模板
    print("測試 5: 獲取查詢模板")
    template = validator.get_query_template('get_trait_scores')
    if template:
        print("特質分數查詢模板:")
        print(template)
