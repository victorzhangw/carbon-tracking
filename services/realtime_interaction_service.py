#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即時語音互動服務
整合 Qwen-ASR-Realtime + DeepSeek LLM + Qwen TTS Realtime
基於官方 WebSocket 範例改寫
"""

import os
import json
import base64
import time
import websocket
import threading
from typing import Callable, Optional
from services.ai import analyze_and_respond_with_context

try:
    import dashscope
    DASHSCOPE_AVAILABLE = True
    dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
except ImportError:
    dashscope = None
    DASHSCOPE_AVAILABLE = False

# 簡繁轉換
def convert_simplified_to_traditional(text: str) -> str:
    """
    將簡體中文轉換為繁體中文
    使用簡單的字典映射方式
    """
    try:
        # 嘗試使用 opencc（如果已安裝）
        import opencc
        converter = opencc.OpenCC('s2t')  # 移除 .json 後綴
        return converter.convert(text)
    except Exception as e:
        # 如果 opencc 失敗，使用內建的簡單映射
        print(f"⚠️ OpenCC 轉換失敗，使用內建映射: {e}")
        # 這裡只處理常見字，完整版需要更大的字典
        simplified_to_traditional = {
            '你': '你', '好': '好', '我': '我', '是': '是', '的': '的',
            '了': '了', '在': '在', '有': '有', '个': '個', '人': '人',
            '这': '這', '那': '那', '来': '來', '去': '去', '说': '說',
            '会': '會', '能': '能', '要': '要', '可': '可', '以': '以',
            '吗': '嗎', '呢': '呢', '啊': '啊', '吧': '吧', '么': '麼',
            '为': '為', '什': '什', '时': '時', '候': '候', '间': '間',
            '听': '聽', '见': '見', '觉': '覺', '得': '得', '对': '對',
            '没': '沒', '还': '還', '也': '也', '都': '都', '很': '很',
            '请': '請', '谢': '謝', '帮': '幫', '助': '助', '问': '問',
            '题': '題', '应': '應', '该': '該', '让': '讓',
            '给': '給', '从': '從', '现': '現', '发': '發', '开': '開',
            '关': '關', '门': '門', '们': '們', '她': '她', '他': '他',
            '它': '它', '您': '您', '咱': '咱', '俩': '倆', '两': '兩',
            '几': '幾', '哪': '哪', '怎': '怎', '样': '樣', '呀': '呀',
        }
        result = []
        for char in text:
            result.append(simplified_to_traditional.get(char, char))
        return ''.join(result)


class RealtimeInteractionService:
    """即時語音互動服務"""
    
    def __init__(self, api_key: str, voice: str = "Nofish"):
        """
        初始化服務
        
        Args:
            api_key: DashScope API 密鑰
            voice: 語音角色 ("Roy" 或 "Nofish")
        """
        self.api_key = api_key
        self.voice = voice
        self.asr_ws = None
        self.tts_ws = None
        self.conversation_context = []
        self.is_running = False
        self.model = "qwen3-asr-flash-realtime"
        
        # 回調函數
        self.on_transcript_partial = None
        self.on_transcript_final = None
        self.on_llm_response = None
        self.on_audio_output = None
        self.on_error = None
        
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 庫未安裝")
    
    def start_asr_session(self):
        """啟動 ASR WebSocket 連接"""
        try:
            # 按照官方範例格式構建 URL 和 headers
            base_url = "wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime"
            url = f"{base_url}?model={self.model}"
            
            # 設置 headers（注意格式：列表形式）
            headers = [
                f"Authorization: Bearer {self.api_key}",
                "OpenAI-Beta: realtime=v1"
            ]
            
            print(f"🔗 連接到 ASR 服務: {url}")
            
            self.asr_ws = websocket.WebSocketApp(
                url,
                header=headers,
                on_open=self._on_asr_open,
                on_message=self._on_asr_message,
                on_error=self._on_asr_error,
                on_close=self._on_asr_close
            )
            
            # 在新線程中運行
            self.is_running = True
            asr_thread = threading.Thread(target=self.asr_ws.run_forever)
            asr_thread.daemon = True
            asr_thread.start()
            
            print(f"✅ ASR WebSocket 連接已啟動")
            return True
        except Exception as e:
            print(f"❌ ASR 連接失敗: {e}")
            if self.on_error:
                self.on_error(f"ASR 連接失敗: {str(e)}")
            return False
    
    def _on_asr_open(self, ws):
        """ASR 連接建立"""
        print("🎤 ASR 連接已建立")
        
        # 發送 session.update 配置（使用 server_vad 模式）
        session_update = {
            "event_id": "session_init",
            "type": "session.update",
            "session": {
                "modalities": ["text"],
                "input_audio_format": "pcm",
                "sample_rate": 16000,
                "input_audio_transcription": {
                    "language": "zh"
                },
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.2,
                    "silence_duration_ms": 800
                }
            }
        }
        
        print(f"📤 發送會話配置: {json.dumps(session_update, ensure_ascii=False)}")
        ws.send(json.dumps(session_update))
    
    def _on_asr_message(self, ws, message):
        """處理 ASR 訊息"""
        try:
            data = json.loads(message)
            event_type = data.get('type')
            
            print(f"📨 收到事件: {event_type}")
            
            if event_type == 'session.created':
                # 會話創建成功
                session_id = data.get('session', {}).get('id', '')
                print(f"✅ 會話已創建: {session_id}")
            
            elif event_type == 'session.updated':
                # 會話配置更新成功
                print(f"✅ 會話配置已更新")
            
            elif event_type == 'conversation.item.input_audio_transcription.text':
                # 即時辨識結果（partial/stash）
                text = data.get('text', '')
                stash = data.get('stash', '')
                # 轉換為繁體中文
                text_traditional = convert_simplified_to_traditional(text)
                stash_traditional = convert_simplified_to_traditional(stash)
                print(f"📝 即時辨識: text={text_traditional}, stash={stash_traditional}")
                if self.on_transcript_partial:
                    self.on_transcript_partial(text_traditional, stash_traditional)
            
            elif event_type == 'conversation.item.input_audio_transcription.completed':
                # 最終辨識結果
                transcript = data.get('transcript', '')
                # 轉換為繁體中文
                transcript_traditional = convert_simplified_to_traditional(transcript)
                print(f"✅ 辨識完成: {transcript_traditional}")
                
                if self.on_transcript_final:
                    self.on_transcript_final(transcript_traditional)
                
                # 觸發 LLM 處理
                if transcript_traditional.strip():
                    self._process_with_llm(transcript_traditional)
            
            elif event_type == 'input_audio_buffer.speech_started':
                print("🎤 檢測到語音開始")
            
            elif event_type == 'input_audio_buffer.speech_stopped':
                print("🎤 檢測到語音結束")
            
            elif event_type == 'error':
                error_msg = data.get('error', {}).get('message', 'Unknown error')
                print(f"❌ ASR 錯誤: {error_msg}")
                if self.on_error:
                    self.on_error(f"ASR 錯誤: {error_msg}")
        
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析錯誤: {e}")
        except Exception as e:
            print(f"❌ ASR 訊息處理錯誤: {e}")
    
    def _on_asr_error(self, ws, error):
        """ASR 錯誤處理"""
        print(f"❌ ASR WebSocket 錯誤: {error}")
        if self.on_error:
            self.on_error(f"ASR 錯誤: {str(error)}")
    
    def _on_asr_close(self, ws, close_status_code, close_msg):
        """ASR 連接關閉"""
        print(f"🔌 ASR 連接已關閉: {close_status_code} - {close_msg}")
    
    def process_audio_input(self, audio_base64: str):
        """
        處理音頻輸入（發送到 ASR）
        
        Args:
            audio_base64: Base64 編碼的 PCM 音頻
        """
        if not self.asr_ws or not self.asr_ws.sock or not self.asr_ws.sock.connected:
            print("❌ ASR 連接未建立或已斷開")
            return False
        
        try:
            # 按照官方範例格式發送音頻
            append_event = {
                "event_id": f"event_{int(time.time() * 1000)}",
                "type": "input_audio_buffer.append",
                "audio": audio_base64
            }
            self.asr_ws.send(json.dumps(append_event))
            return True
        except Exception as e:
            print(f"❌ 發送音頻失敗: {e}")
            return False
    
    def _process_with_llm(self, user_text: str):
        """
        使用 LLM 生成回應
        
        Args:
            user_text: 用戶輸入文字
        """
        try:
            print(f"🤖 LLM 處理中: {user_text}")
            
            # 使用專案既有的 LLM 服務
            result = analyze_and_respond_with_context(
                user_input=user_text,
                conversation_context=self.conversation_context,
                response_style='friendly',
                conversation_mode='continuous',
                conversation_round=len(self.conversation_context) // 2
            )
            
            response_text = result.get('response', '')
            sentiment = result.get('sentiment', '未知')
            confidence = result.get('confidence', 0.0)
            
            print(f"✅ LLM 回應: {response_text}")
            
            # 更新對話上下文
            self.conversation_context.append({
                'role': 'user',
                'content': user_text
            })
            self.conversation_context.append({
                'role': 'assistant',
                'content': response_text
            })
            
            # 保留最近 10 輪對話
            if len(self.conversation_context) > 20:
                self.conversation_context = self.conversation_context[-20:]
            
            # 回調 LLM 回應
            if self.on_llm_response:
                self.on_llm_response(response_text, sentiment, confidence)
            
            # 觸發 TTS 合成
            self._synthesize_with_tts(response_text)
        
        except Exception as e:
            print(f"❌ LLM 處理錯誤: {e}")
            if self.on_error:
                self.on_error(f"LLM 處理錯誤: {str(e)}")
    
    def _synthesize_with_tts(self, text: str):
        """
        使用 TTS 合成語音（流式）
        使用 Qwen TTS Flash 模型進行流式輸出
        
        Args:
            text: 要合成的文字
        """
        try:
            print(f"🎵 TTS 合成中: {text[:50]}...")
            print(f"🎵 使用語音: {self.voice}")
            
            # 限制文本長度
            if len(text) > 200:
                text = text[:200]
            
            # 使用 Qwen TTS API（流式）
            # 注意：使用 qwen3-tts-flash 而非 qwen3-tts-flash-realtime
            # realtime 版本需要 WebSocket，而 HTTP API 使用標準版本
            print(f"🎵 調用 TTS API...")
            response = dashscope.MultiModalConversation.call(
                api_key=self.api_key,
                model="qwen3-tts-flash",
                text=text,
                voice=self.voice,
                language_type="Chinese",
                stream=True
            )
            
            print(f"🎵 開始接收音頻流...")
            
            # 流式發送音頻
            audio_chunks_received = 0
            for chunk in response:
                print(f"🎵 收到 chunk: {type(chunk)}")
                
                # 檢查是否有錯誤
                if hasattr(chunk, 'code') and chunk.code:
                    error_msg = f"TTS 錯誤代碼: {chunk.code}"
                    if hasattr(chunk, 'message'):
                        error_msg += f", 訊息: {chunk.message}"
                    print(f"❌ {error_msg}")
                    if self.on_error:
                        self.on_error(error_msg)
                    return
                
                # 處理音頻數據
                if chunk.output is not None:
                    print(f"🎵 chunk.output 存在")
                    audio = chunk.output.audio
                    if audio is not None:
                        print(f"🎵 audio 存在")
                        if audio.data is not None:
                            # 發送音頻數據（Base64 編碼的 PCM 數據）
                            audio_chunks_received += 1
                            print(f"🎵 發送音頻塊 #{audio_chunks_received}, 大小: {len(audio.data)}")
                            if self.on_audio_output:
                                self.on_audio_output(audio.data, False)
                        else:
                            print(f"⚠️ audio.data 為 None")
                    else:
                        print(f"⚠️ audio 為 None")
                    
                    # 檢查是否完成
                    if hasattr(chunk.output, 'finish_reason') and chunk.output.finish_reason == "stop":
                        print(f"✅ TTS 合成完成 (收到 {audio_chunks_received} 個音頻塊)")
                        break
                else:
                    print(f"⚠️ chunk.output 為 None")
            
            # 發送結束標記
            if self.on_audio_output:
                self.on_audio_output(None, True)
                print(f"🎵 已發送結束標記")
        
        except Exception as e:
            print(f"❌ TTS 合成錯誤: {e}")
            import traceback
            traceback.print_exc()
            if self.on_error:
                self.on_error(f"TTS 合成錯誤: {str(e)}")
    
    def close_sessions(self):
        """關閉所有連接"""
        self.is_running = False
        
        if self.asr_ws:
            try:
                self.asr_ws.close()
                print("✅ ASR 連接已關閉")
            except:
                pass
        
        self.conversation_context = []
        print("✅ 會話已清理")
