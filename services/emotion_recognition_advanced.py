import torch
import librosa
import numpy as np
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
import warnings
warnings.filterwarnings("ignore")

class AdvancedEmotionRecognizer:
    def __init__(self):
        self.model_name = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
        self.model = None
        self.feature_extractor = None
        self.emotion_labels = {
            0: "angry",
            1: "calm", 
            2: "disgust",
            3: "fearful",
            4: "happy",
            5: "neutral",
            6: "sad",
            7: "surprised"
        }
        
    def load_model(self):
        """載入預訓練模型"""
        try:
            self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(self.model_name)
            self.model = Wav2Vec2ForSequenceClassification.from_pretrained(self.model_name)
            print("✅ 情緒識別模型載入成功")
            return True
        except Exception as e:
            print(f"❌ 模型載入失敗: {e}")
            return False
    
    def predict_emotion(self, audio_path):
        """使用深度學習模型預測情緒"""
        try:
            # 如果模型未載入，嘗試載入
            if self.model is None:
                if not self.load_model():
                    return {"error": "模型載入失敗"}
            
            # 載入音頻
            speech, sample_rate = librosa.load(audio_path, sr=16000)
            
            # 預處理音頻
            inputs = self.feature_extractor(
                speech, 
                sampling_rate=sample_rate, 
                return_tensors="pt", 
                padding=True
            )
            
            # 預測
            with torch.no_grad():
                logits = self.model(**inputs).logits
                probabilities = torch.nn.functional.softmax(logits, dim=-1)
                predicted_id = torch.argmax(logits, dim=-1).item()
            
            # 建立結果
            predicted_emotion = self.emotion_labels[predicted_id]
            confidence = probabilities[0][predicted_id].item()
            
            # 所有情緒的機率
            all_emotions = {
                self.emotion_labels[i]: float(probabilities[0][i]) 
                for i in range(len(self.emotion_labels))
            }
            
            return {
                "predicted_emotion": predicted_emotion,
                "confidence": float(confidence),
                "all_emotions": all_emotions,
                "model": "wav2vec2-emotion-recognition"
            }
            
        except Exception as e:
            return {"error": f"情緒預測失敗: {str(e)}"}

# 全域實例
advanced_emotion_recognizer = AdvancedEmotionRecognizer()