"""測試 TTS 服務"""
import sys
sys.path.insert(0, '.')

from services.tts import gpt_sovits_tts

# 測試生成語音
text = "您好，今天天氣很好"
print(f"測試文字: {text}")
print(f"TTS API URL: {gpt_sovits_tts.api_url}")
print(f"參考音頻: {gpt_sovits_tts.default_ref_audio}")

result = gpt_sovits_tts.generate_speech(text)
if result:
    print(f"✅ 成功: {result}")
else:
    print("❌ 失敗")
