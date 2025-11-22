import os
import json
from openai import OpenAI
from config import DEEPSEEK_API_KEY, BASE_URL, MODEL_NAME
from utils import fix_incomplete_json
from services.gpt_sovits_service import gpt_sovits_service
from database import save_voice_generation_record

# 初始化  AI 客戶端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=BASE_URL,
)

def analyze_and_respond(transcript):
    """分析文字內容並生成回應 - 兼容旧版本"""
    return analyze_and_respond_with_context(transcript)

def analyze_and_respond_with_context(user_input, conversation_context=None, response_style='friendly', conversation_mode='continuous', conversation_round=0):
    """增强版AI分析 - 支持多轮对话上下文"""
    try:
        # 构建系统提示词
        system_prompt = build_system_prompt(response_style, conversation_mode, conversation_round)
        
        # 构建消息历史
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加对话上下文
        if conversation_context and len(conversation_context) > 0:
            for ctx_msg in conversation_context[-6:]:  # 保留最近6条消息
                messages.append({
                    "role": ctx_msg.get('role', 'user'),
                    "content": ctx_msg.get('content', '')
                })
        
        # 添加当前用户输入
        user_prompt = build_user_prompt(user_input, conversation_round, len(conversation_context) if conversation_context else 0)
        messages.append({"role": "user", "content": user_prompt})
        
        print(f"🤖 請求 Message 數量 : {len(messages)}")
        print(f"📝 系統提示: {system_prompt[:100]}...")
        
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=600,
            temperature=get_temperature_by_style(response_style)
        )
        
        message_content = completion.choices[0].message.content
        clean_content = message_content.replace('``` json\n', '').replace('\n ```', '')
        fixed_json = fix_incomplete_json(clean_content)
        
        try:
            data = json.loads(fixed_json)
            sentiment = data.get('sentiment', '未知')
            response = data.get('response', '無法解析回應內容')
            confidence = data.get('confidence', 0.95)
            
            # 不在這裡生成語音，改為在voice_clone路由中處理
            audio_url = None
            
            return {
                "sentiment": sentiment, 
                "response": response, 
                "confidence": confidence,
                "audio_url": audio_url
            }
                
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            return {
                "sentiment": "未知", 
                "response": f"JSON 解析錯誤: {str(e)}", 
                "confidence": 0.5,
                "audio_url": None
            }
            
        except Exception as e:
            print(f"處理回應時發生錯誤: {e}")
            return {
                "sentiment": "未知", 
                "response": f"處理回應時發生錯誤: {str(e)}", 
                "confidence": 0.5,
                "audio_url": None
            }
    
    except Exception as e:
        print(f"OpenAI API 請求錯誤: {e}")
        return {
            "sentiment": "未知", 
            "response": "生成回應時發生錯誤，請重試。", 
            "confidence": 0.5,
            "audio_url": None
        }

def build_system_prompt(response_style, conversation_mode, conversation_round):
    """构建系统提示词"""
    base_prompt = (
        "你是一位專業的社會服務的人員，擅長諮商輔導並具有豐富的知識背景。"
        "請以同理心和專業的態度提供建議，特別注意使用適合的中文表達方式，不能中英文夾雜，以及使用一些語助詞。"
    )
    
    # 根据回应风格调整
    style_prompts = {
        'friendly': "語氣要友好親切，像朋友般交談，使用台灣當地口語，避免過於正式的敬語，不能中英文夾雜使用。",
        'professional': "保持專業正式的語調，使用準確的專業術語，但要確保用戶能理解，不能中英文夾雜使用。",
        'casual': "使用輕鬆隨意的語調，可以適當使用網路用語和表情符號，不能中英文夾雜使用。",
        'detailed': "提供詳細的解說和分析，包含背景知識和具體的操作建議，不能中英文夾雜使用。"
    }
    
    # 根据对话模式调整
    mode_prompts = {
        'continuous': "這是一個連續對話，請參考之前的對話內容，保持話題的連貫性。",
        'qa': "這是問答模式，專注於回答用戶的具體問題。",
        'creative': "這是創意模式，可以提供更多創新的想法和建議。"
    }
    
    # 根据对话轮次调整
    if conversation_round == 0:
        round_prompt = "這是對話的開始，請友好地打招呼並了解用戶需求。"
    elif conversation_round < 3:
        round_prompt = "這是對話的前期階段，請深入了解用戶的情況。"
    else:
        round_prompt = "這是深度對話階段，請基於之前的交流提供更具體的建議。"
    
    full_prompt = f"{base_prompt}\n{style_prompts.get(response_style, style_prompts['friendly'])}\n{mode_prompts.get(conversation_mode, mode_prompts['continuous'])}\n{round_prompt}\n回應字數控制在150-250個中文字之間。"
    
    return full_prompt

def build_user_prompt(user_input, conversation_round, context_count):
    """构建用户提示词"""
    if conversation_round == 0:
        context_info = "這是我們對話的開始。"
    else:
        context_info = f"這是我們對話的第{conversation_round + 1}輪，之前已經交流了{context_count}條消息。"
    
    return f"{context_info}用戶說：\"{user_input}\"。請分析用戶的情緒（正面、中性、負面、積極、消極等），評估回應的置信度（0-1之間的數值），並基於對話上下文提供適當的回應。使用JSON格式回應，包含sentiment、confidence和response三個欄位。"

def get_temperature_by_style(response_style):
    """根据回应风格获取temperature参数"""
    temperature_map = {
        'friendly': 0.8,
        'professional': 0.5,
        'casual': 0.9,
        'detailed': 0.6
    }
    return temperature_map.get(response_style, 0.7)

def generate_care_message(schedule, weather_info, user_profile):
    """
    生成定期關懷訊息（使用 DeepSeek LLM）
    
    Args:
        schedule (dict): 排程資訊
        weather_info (dict): 天氣資訊
        user_profile (dict): 用戶資料
    
    Returns:
        str: 關懷訊息文本
    """
    try:
        # 構建系統提示詞
        system_prompt = """你是一位溫暖關懷的社工人員，專門為長者提供定期關懷服務。
你的任務是生成一段溫馨、自然的關懷訊息。

要求：
1. 語氣親切溫暖，像家人般關心
2. 使用台灣當地口語，自然流暢
3. 根據天氣提供實用建議
4. 關注長者的健康和安全
5. 字數控制在 150-200 字
6. 不要使用過於正式的敬語
7. 可以適當使用語助詞（喔、呢、啦等）
8. 不要中英文夾雜"""
        
        # 構建用戶訊息
        user_name = user_profile.get('full_name', '長者')
        user_age = user_profile.get('age', '70')
        health_notes = user_profile.get('health_notes', '良好')
        
        scheduled_time = schedule.get('scheduled_time', '')
        address = schedule.get('address', '家中')
        description = schedule.get('description', '')
        
        condition = weather_info.get('condition', '晴朗')
        temperature = weather_info.get('temperature', 25)
        
        user_message = f"""請為以下長者生成一段關懷訊息：

長者資訊：
- 姓名：{user_name}
- 年齡：{user_age}歲
- 健康狀況：{health_notes}

當前情境：
- 時間：{scheduled_time}
- 地點：{address}
- 天氣：{condition}
- 溫度：{temperature}度
- 特別提醒：{description if description else '無'}

請生成一段溫馨的關懷訊息。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=400,
            temperature=0.8
        )
        
        message = completion.choices[0].message.content.strip()
        
        # 確保訊息長度適中（Qwen TTS 限制 200 字符）
        if len(message) > 200:
            message = message[:200]
        
        return message
        
    except Exception as e:
        print(f"生成關懷訊息失敗: {e}")
        # 返回預設訊息
        return f"{user_profile.get('full_name', '長者')}您好，這是一則溫馨的關懷提醒。今天天氣{weather_info.get('condition', '不錯')}，溫度約{weather_info.get('temperature', 25)}度，請注意保重身體。祝您有美好的一天！"
