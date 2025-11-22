"""直接測試 GPT-SoVITS API"""
import requests
import json

url = "http://127.0.0.1:9880/tts"
payload = {
    "text": "您好，今天天氣很好，很高興為您服務",
    "text_lang": "zh",
    "ref_audio_path": "TTS/vc.wav",
    "prompt_lang": "zh",
    "prompt_text": "使用軟件者、傳播軟件導出的聲音者自負全責。如不認可該條款，則不能使用或引用軟件",
    "batch_size": 20,
    "text_split_method": "cut5",
    "batch_threshold": 0.75,
    "streaming_mode": False,
    "temperature": 1.1
}

print("發送請求...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)

print(f"\n狀態碼: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content-Length: {len(response.content)} bytes")

if response.status_code == 200:
    # 保存音頻
    with open('test_output.wav', 'wb') as f:
        f.write(response.content)
    print("✅ 成功！音頻已保存到 test_output.wav")
else:
    print(f"❌ 失敗: {response.text}")
