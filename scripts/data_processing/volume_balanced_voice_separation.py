#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音量平衡的人聲分離工具
解決分離後個人音量忽高忽低的問題
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import os
import sys
import librosa
import soundfile as sf
import numpy as np
from scipy import signal
from scipy.ndimage import uniform_filter1d
import noisereduce as nr
from pydub import AudioSegment
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path

class VolumeBalancedVoiceSeparator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_dir = Path(input_file).parent / "volume_balanced_audio"
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_to_wav(self):
        """轉換為 WAV 格式"""
        try:
            audio = AudioSegment.from_file(self.input_file)
            wav_path = self.output_dir / f"{Path(self.input_file).stem}_converted.wav"
            audio.export(wav_path, format="wav")
            print(f"✓ 音頻已轉換為 WAV 格式: {wav_path}")
            return str(wav_path)
        except Exception as e:
            print(f"✗ 轉換失敗: {e}")
            return None
    
    def load_audio(self, file_path):
        """載入音頻檔案"""
        try:
            y, sr = librosa.load(file_path, sr=None)
            print(f"✓ 音頻載入成功 - 採樣率: {sr}Hz, 長度: {len(y)/sr:.2f}秒")
            return y, sr
        except Exception as e:
            print(f"✗ 音頻載入失敗: {e}")
            return None, None
    
    def gentle_noise_reduction(self, y, sr):
        """溫和的噪音減少"""
        try:
            y_clean = nr.reduce_noise(
                y=y, 
                sr=sr, 
                stationary=True, 
                prop_decrease=0.15,
                n_std_thresh_stationary=2.0,
                n_fft=1024
            )
            print("✓ 溫和噪音減少完成")
            return y_clean
        except Exception as e:
            print(f"✗ 噪音減少失敗: {e}")
            return y
    
    def extract_speaker_features(self, y, sr):
        """提取說話者特徵，用於更準確的分離"""
        try:
            # 使用較小的窗口以獲得更好的時間解析度
            frame_length = 1024
            hop_length = 256
            
            # 提取 MFCC 特徵
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, 
                                       n_fft=frame_length, hop_length=hop_length)
            
            # 提取基頻
            f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                       fmin=librosa.note_to_hz('C2'), 
                                                       fmax=librosa.note_to_hz('C7'),
                                                       frame_length=frame_length)
            
            # 提取頻譜重心
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, 
                                                                 hop_length=hop_length)[0]
            
            # 提取 RMS 能量
            rms = librosa.feature.rms(y=y, frame_length=frame_length, 
                                    hop_length=hop_length)[0]
            
            print("✓ 說話者特徵提取完成")
            return {
                'mfccs': mfccs,
                'f0': f0,
                'voiced_flag': voiced_flag,
                'spectral_centroids': spectral_centroids,
                'rms': rms,
                'hop_length': hop_length
            }
            
        except Exception as e:
            print(f"✗ 特徵提取失敗: {e}")
            return None
    
    def intelligent_speaker_separation(self, y, sr, features, n_speakers=2):
        """智能說話者分離，基於多維特徵"""
        try:
            print(f"開始智能分離 {n_speakers} 個說話者...")
            
            mfccs = features['mfccs']
            f0 = features['f0']
            spectral_centroids = features['spectral_centroids']
            rms = features['rms']
            
            # 準備聚類特徵矩陣
            feature_matrix = []
            valid_indices = []
            
            # 只使用有語音活動的幀
            for i in range(mfccs.shape[1]):
                if i < len(rms) and rms[i] > np.percentile(rms, 20):  # 能量閾值
                    frame_features = []
                    
                    # MFCC 特徵 (前8個係數)
                    frame_features.extend(mfccs[:8, i])
                    
                    # 基頻特徵
                    if i < len(f0) and not np.isnan(f0[i]):
                        frame_features.append(f0[i])
                    else:
                        frame_features.append(0)
                    
                    # 頻譜重心
                    if i < len(spectral_centroids):
                        frame_features.append(spectral_centroids[i])
                    
                    # RMS 能量
                    frame_features.append(rms[i])
                    
                    feature_matrix.append(frame_features)
                    valid_indices.append(i)
            
            if len(feature_matrix) < n_speakers:
                print("✗ 有效語音幀數不足")
                return None
            
            # 標準化特徵
            feature_matrix = np.array(feature_matrix)
            scaler = StandardScaler()
            feature_matrix_scaled = scaler.fit_transform(feature_matrix)
            
            # K-means 聚類
            kmeans = KMeans(n_clusters=n_speakers, random_state=42, n_init=20)
            speaker_labels = kmeans.fit_predict(feature_matrix_scaled)
            
            print(f"✓ 智能說話者分離完成，識別出 {len(np.unique(speaker_labels))} 個說話者")
            
            return {
                'speaker_labels': speaker_labels,
                'valid_indices': valid_indices,
                'rms': rms,
                'hop_length': features['hop_length']
            }
            
        except Exception as e:
            print(f"✗ 說話者分離失敗: {e}")
            return None
    
    def create_volume_balanced_masks(self, y, sr, separation_result):
        """創建音量平衡的說話者遮罩"""
        try:
            speaker_labels = separation_result['speaker_labels']
            valid_indices = separation_result['valid_indices']
            rms = separation_result['rms']
            hop_length = separation_result['hop_length']
            
            n_frames = len(rms)
            n_speakers = len(np.unique(speaker_labels))
            
            # 初始化說話者遮罩
            speaker_masks = np.zeros((n_speakers, n_frames))
            speaker_energies = np.zeros((n_speakers, n_frames))
            
            # 填充說話者標籤和能量
            label_idx = 0
            for frame_idx in range(n_frames):
                if frame_idx in valid_indices and label_idx < len(speaker_labels):
                    speaker_id = speaker_labels[label_idx]
                    speaker_masks[speaker_id, frame_idx] = 1.0
                    speaker_energies[speaker_id, frame_idx] = rms[frame_idx]
                    label_idx += 1
            
            # 平滑遮罩
            for speaker_id in range(n_speakers):
                # 使用較大的平滑窗口
                speaker_masks[speaker_id] = uniform_filter1d(speaker_masks[speaker_id], size=15)
                
                # 應用 sigmoid 函數使過渡更平滑
                speaker_masks[speaker_id] = 1 / (1 + np.exp(-8 * (speaker_masks[speaker_id] - 0.5)))
                
                # 確保最小值，保持連續性
                speaker_masks[speaker_id] = np.maximum(speaker_masks[speaker_id], 0.05)
            
            print(f"✓ 創建了 {n_speakers} 個音量平衡遮罩")
            return speaker_masks, speaker_energies, hop_length
            
        except Exception as e:
            print(f"✗ 創建遮罩失敗: {e}")
            return None, None, None
    
    def apply_volume_balanced_separation(self, y, sr, speaker_masks, speaker_energies, hop_length):
        """應用音量平衡的說話者分離"""
        try:
            # 計算 STFT
            D = librosa.stft(y, hop_length=hop_length, n_fft=2048)
            magnitude, phase = np.abs(D), np.angle(D)
            
            separated_audios = []
            n_speakers = speaker_masks.shape[0]
            
            for speaker_id in range(n_speakers):
                # 調整遮罩大小以匹配 STFT
                mask = speaker_masks[speaker_id]
                if len(mask) != magnitude.shape[1]:
                    mask = np.interp(np.linspace(0, len(mask)-1, magnitude.shape[1]), 
                                   np.arange(len(mask)), mask)
                
                # 應用遮罩
                masked_magnitude = magnitude * mask[np.newaxis, :]
                
                # 重建音頻
                masked_stft = masked_magnitude * np.exp(1j * phase)
                separated_audio = librosa.istft(masked_stft, hop_length=hop_length, length=len(y))
                
                separated_audios.append(separated_audio)
            
            print(f"✓ 音量平衡分離完成，生成 {len(separated_audios)} 個說話者音頻")
            return separated_audios
            
        except Exception as e:
            print(f"✗ 音頻分離失敗: {e}")
            return None 
   
    def normalize_speaker_volume(self, audio, target_rms=0.02):
        """正規化說話者音量，解決忽高忽低問題"""
        try:
            # 計算當前 RMS
            current_rms = np.sqrt(np.mean(audio ** 2))
            
            if current_rms > 0:
                # 計算正規化因子
                normalization_factor = target_rms / current_rms
                normalized_audio = audio * normalization_factor
            else:
                normalized_audio = audio
            
            # 應用動態範圍壓縮，平滑音量變化
            compressed_audio = self.apply_dynamic_range_compression(normalized_audio)
            
            print("✓ 說話者音量正規化完成")
            return compressed_audio
            
        except Exception as e:
            print(f"✗ 音量正規化失敗: {e}")
            return audio
    
    def apply_dynamic_range_compression(self, y, threshold=0.1, ratio=3.0, attack_time=0.01, release_time=0.1):
        """應用動態範圍壓縮，平滑音量變化"""
        try:
            # 計算包絡
            envelope = np.abs(y)
            
            # 平滑包絡
            sr = 16000  # 假設採樣率
            attack_samples = int(attack_time * sr)
            release_samples = int(release_time * sr)
            
            # 簡化的壓縮器
            compressed = y.copy()
            gain_reduction = np.ones_like(y)
            
            for i in range(len(envelope)):
                if envelope[i] > threshold:
                    # 計算增益減少
                    excess = envelope[i] - threshold
                    gain_reduction[i] = threshold + excess / ratio
                    gain_reduction[i] = gain_reduction[i] / envelope[i] if envelope[i] > 0 else 1
                
            # 平滑增益變化
            gain_reduction = uniform_filter1d(gain_reduction, size=attack_samples)
            
            # 應用增益
            compressed = y * gain_reduction
            
            return compressed
            
        except Exception as e:
            print(f"✗ 動態範圍壓縮失敗: {e}")
            return y
    
    def apply_volume_smoothing(self, y, sr, window_size=0.1):
        """應用音量平滑，減少突兀的音量變化"""
        try:
            # 計算短時 RMS
            frame_length = int(window_size * sr)
            hop_length = frame_length // 4
            
            # 計算 RMS 包絡
            rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
            
            # 平滑 RMS
            smoothed_rms = uniform_filter1d(rms, size=5)
            
            # 重新採樣到原始長度
            time_frames = np.arange(len(rms)) * hop_length
            time_samples = np.arange(len(y))
            
            # 插值到樣本級別
            smoothed_envelope = np.interp(time_samples, time_frames, smoothed_rms)
            
            # 計算原始包絡
            original_envelope = np.abs(y)
            original_envelope = uniform_filter1d(original_envelope, size=frame_length//10)
            
            # 計算增益調整
            gain_adjustment = np.ones_like(y)
            for i in range(len(y)):
                if original_envelope[i] > 0:
                    gain_adjustment[i] = smoothed_envelope[i] / original_envelope[i]
                    # 限制增益變化範圍
                    gain_adjustment[i] = np.clip(gain_adjustment[i], 0.5, 2.0)
            
            # 應用平滑增益
            y_smoothed = y * gain_adjustment
            
            print("✓ 音量平滑處理完成")
            return y_smoothed
            
        except Exception as e:
            print(f"✗ 音量平滑失敗: {e}")
            return y
    
    def save_audio(self, audio_data, sr, filename):
        """儲存音頻檔案"""
        try:
            output_path = self.output_dir / filename
            sf.write(output_path, audio_data, sr)
            print(f"✓ 音頻已儲存: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"✗ 音頻儲存失敗: {e}")
            return None
    
    def process_audio(self, n_speakers=2):
        """主要處理流程 - 音量平衡優先"""
        print(f"🎵 開始音量平衡音頻處理 - 分離 {n_speakers} 個說話者")
        print("🔊 專門解決音量忽高忽低問題")
        print("=" * 60)
        print(f"處理檔案: {self.input_file}")
        
        # 1. 轉換格式
        wav_file = self.convert_to_wav()
        if not wav_file:
            return False
        
        # 2. 載入音頻
        y, sr = self.load_audio(wav_file)
        if y is None:
            return False
        
        # 3. 溫和的噪音減少
        y_clean = self.gentle_noise_reduction(y, sr)
        
        # 4. 提取說話者特徵
        features = self.extract_speaker_features(y_clean, sr)
        if features is None:
            return False
        
        # 5. 智能說話者分離
        separation_result = self.intelligent_speaker_separation(y_clean, sr, features, n_speakers)
        if separation_result is None:
            # 如果分離失敗，至少提供音量平衡的整體音頻
            y_balanced = self.normalize_speaker_volume(y_clean)
            y_smoothed = self.apply_volume_smoothing(y_balanced, sr)
            
            results = {}
            results['original'] = self.save_audio(y, sr, "01_original.wav")
            results['volume_balanced'] = self.save_audio(y_smoothed, sr, "02_volume_balanced.wav")
            
            print("\n" + "=" * 60)
            print("⚠️ 說話者分離失敗，但已生成音量平衡版本")
            return True
        
        # 6. 創建音量平衡遮罩
        speaker_masks, speaker_energies, hop_length = self.create_volume_balanced_masks(
            y_clean, sr, separation_result)
        if speaker_masks is None:
            return False
        
        # 7. 應用音量平衡分離
        separated_audios = self.apply_volume_balanced_separation(
            y_clean, sr, speaker_masks, speaker_energies, hop_length)
        if separated_audios is None:
            return False
        
        # 8. 對每個說話者應用音量處理
        balanced_speakers = []
        for i, speaker_audio in enumerate(separated_audios):
            # 正規化音量
            normalized = self.normalize_speaker_volume(speaker_audio)
            # 應用音量平滑
            smoothed = self.apply_volume_smoothing(normalized, sr)
            balanced_speakers.append(smoothed)
        
        # 9. 儲存結果
        results = {}
        results['original'] = self.save_audio(y, sr, "01_original.wav")
        results['cleaned'] = self.save_audio(y_clean, sr, "02_noise_reduced.wav")
        
        # 儲存音量平衡的說話者音頻
        for i, (raw_audio, balanced_audio) in enumerate(zip(separated_audios, balanced_speakers)):
            speaker_num = i + 1
            results[f'speaker_{speaker_num}_raw'] = self.save_audio(
                raw_audio, sr, f"03_speaker_{speaker_num}_raw.wav"
            )
            results[f'speaker_{speaker_num}_balanced'] = self.save_audio(
                balanced_audio, sr, f"04_speaker_{speaker_num}_volume_balanced.wav"
            )
        
        # 創建整體音量平衡版本
        if len(balanced_speakers) >= 2:
            mixed_balanced = np.zeros_like(balanced_speakers[0])
            for balanced in balanced_speakers:
                mixed_balanced += balanced * 0.5  # 平均混合
            results['mixed_balanced'] = self.save_audio(
                mixed_balanced, sr, "05_all_speakers_volume_balanced.wav"
            )
        
        print("\n" + "=" * 60)
        print("🎉 音量平衡處理完成！輸出檔案:")
        for key, path in results.items():
            if path:
                print(f"  📁 {key}: {Path(path).name}")
        
        print(f"\n💡 推薦使用 (音量平衡):")
        print(f"  🔊 說話者1: 04_speaker_1_volume_balanced.wav")
        print(f"  🔊 說話者2: 04_speaker_2_volume_balanced.wav")
        print(f"  🔊 整體平衡: 05_all_speakers_volume_balanced.wav")
        
        print(f"\n🌟 特點: 解決音量忽高忽低，保持穩定音量")
        
        return True

def main():
    input_file = r"D:\python\Flask-AICares\TTS\03041966.m4a"
    
    print("🎵 音量平衡人聲分離工具")
    print("=" * 60)
    print("🔊 專門解決的問題:")
    print("  • 分離後個人音量忽高忽低")
    print("  • 音量不穩定")
    print("  • 動態範圍過大")
    print("  • 突兀的音量變化")
    print("=" * 60)
    
    if not os.path.exists(input_file):
        print(f"❌ 檔案不存在: {input_file}")
        return False
    
    try:
        separator = VolumeBalancedVoiceSeparator(input_file)
        success = separator.process_audio(n_speakers=2)
        
        if success:
            print("\n🎉 音量平衡處理完成！")
            print(f"📁 輸出目錄: {separator.output_dir}")
            print("\n📋 檔案說明:")
            print("  🔊 04_speaker_X_volume_balanced.wav - 音量平衡的說話者（推薦）")
            print("  📊 03_speaker_X_raw.wav - 原始分離版本（對比用）")
            print("  🔊 05_all_speakers_volume_balanced.wav - 整體音量平衡版")
            
            print("\n💡 改進效果:")
            print("  • 穩定的音量水平")
            print("  • 平滑的音量過渡")
            print("  • 動態範圍壓縮")
            print("  • 消除突兀變化")
            
            return True
        else:
            print("\n❌ 處理失敗")
            return False
            
    except Exception as e:
        print(f"\n❌ 處理錯誤: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)