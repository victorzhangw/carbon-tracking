import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class EmotionRecognizer:
    def __init__(self):
        self.model = None
        self.emotions = ['neutral', 'happy', 'sad', 'angry', 'fear', 'surprise']
        
    def extract_features(self, audio_path):
        """提取音頻特徵"""
        try:
            # 載入音頻檔案
            y, sr = librosa.load(audio_path, duration=30)
            
            # 提取 MFCC 特徵
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfccs_mean = np.mean(mfccs, axis=1)
            
            # 提取光譜質心
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            spectral_centroids_mean = np.mean(spectral_centroids)
            
            # 提取零交叉率
            zcr = librosa.feature.zero_crossing_rate(y)
            zcr_mean = np.mean(zcr)
            
            # 提取音調和節拍
            try:
                tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            except:
                tempo = 120.0  # 預設值
            
            # 合併所有特徵
            features = np.concatenate([
                mfccs_mean,
                [spectral_centroids_mean, zcr_mean, tempo]
            ])
            
            return features
            
        except Exception as e:
            print(f"特徵提取失敗: {e}")
            return None
    
    def predict_emotion(self, audio_path):
        """預測音頻情緒"""
        if not self.model:
            # 這裡可以載入預訓練模型，或使用簡單的規則
            return self._simple_emotion_detection(audio_path)
        
        features = self.extract_features(audio_path)
        if features is None:
            return {"error": "無法提取音頻特徵"}
        
        # 預測情緒
        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]
        
        # 建立結果字典
        result = {
            "predicted_emotion": self.emotions[prediction],
            "confidence": float(max(probabilities)),
            "all_emotions": {
                emotion: float(prob) 
                for emotion, prob in zip(self.emotions, probabilities)
            }
        }
        
        return result
    
    def _simple_emotion_detection(self, audio_path):
        """簡單的情緒檢測（基於音頻特徵規則）"""
        try:
            # 載入音頻檔案
            y, sr = librosa.load(audio_path, duration=10)
            
            # 計算基本統計特徵
            rms_energy = np.sqrt(np.mean(y**2))
            zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            
            # 嘗試提取節拍
            try:
                tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            except:
                tempo = 120.0
            
            # 基於特徵的簡單分類
            if rms_energy > 0.02 and tempo > 120:
                emotion = "happy"
                confidence = 0.75
            elif rms_energy < 0.01 and tempo < 90:
                emotion = "sad"
                confidence = 0.7
            elif spectral_centroid > 3000 and rms_energy > 0.015:
                emotion = "angry"
                confidence = 0.65
            elif zero_crossing_rate > 0.1:
                emotion = "surprise"
                confidence = 0.6
            else:
                emotion = "neutral"
                confidence = 0.55
            
            return {
                "predicted_emotion": emotion,
                "confidence": confidence,
                "features": {
                    "tempo": float(tempo),
                    "spectral_centroid": float(spectral_centroid),
                    "rms_energy": float(rms_energy),
                    "zero_crossing_rate": float(zero_crossing_rate)
                }
            }
            
        except Exception as e:
            return {"error": f"情緒分析失敗: {str(e)}"}

# 全域實例
emotion_recognizer = EmotionRecognizer()