#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
進階音頻人聲分離和說話者分離工具
專門針對對話場景，保持人聲清晰度並分離不同說話者
"""

import os
import sys
import librosa
import soundfile as sf
import numpy as np
from scipy import signal
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
import noisereduce as nr
from pydub import AudioSegment
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import argparse
from pathlib import Path
import matplotlib.pyplot as plt

class AdvancedVoiceSeparator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_dir = Path(input_file).parent / "advanced_separated_audio"
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_to_wav(self):
        """將 m4a 或其他格式轉換為 wav，保持高品質"""
        try:
            # 使用更高的品質設定
            audio = AudioSegment.from_file(self.input_file)
            # 確保採樣率足夠高以保持語音品質
            if audio.frame_rate < 22050:
                audio = audio.set_frame_rate(22050)
            wav_path = self.output_dir / f"{Path(self.input_file).stem}_converted.wav"
            audio.export(wav_path, format="wav", parameters=["-q:a", "0"])
            print(f"✓ 音頻已轉換為高品質 WAV 格式: {wav_path}")
            return str(wav_path)
        except Exception as e:
            print(f"✗ 轉換失敗: {e}")
            return None
    
    def load_audio(self, file_path):
        """載入音頻檔案，保持原始採樣率"""
        try:
            # 保持原始採樣率以維持品質
            y, sr = librosa.load(file_path, sr=None)
            print(f"✓ 音頻載入成功 - 採樣率: {sr}Hz, 長度: {len(y)/sr:.2f}秒")
            return y, sr
        except Exception as e:
            print(f"✗ 音頻載入失敗: {e}")
            return None, None
    
    def advanced_noise_reduction(self, y, sr):
        """進階噪音減少，專門處理鈴聲和空白片段"""
        try:
            print("開始進階噪音處理...")
            
            # 1. 檢測和去除鈴聲（通常在特定頻率範圍）
            y_no_ring = self.remove_ring_tones(y, sr)
            
            # 2. 去除空白和低能量片段
            y_trimmed = self.remove_silence_segments(y_no_ring, sr)
            
            # 3. 多階段噪音減少
            # 第一階段：強力去除穩定噪音
            y_stage1 = nr.reduce_noise(
                y=y_trimmed, 
                sr=sr, 
                stationary=True, 
                prop_decrease=0.7,  # 較強的減少
                n_std_thresh_stationary=1.0,
                n_fft=2048
            )
            
            # 第二階段：去除非穩定噪音
            y_stage2 = nr.reduce_noise(
                y=y_stage1, 
                sr=sr, 
                stationary=False, 
                prop_decrease=0.5,
                n_std_thresh_stationary=1.2,
                n_fft=1024
            )
            
            # 4. 頻域濾波去除特定噪音
            y_filtered = self.apply_noise_filters(y_stage2, sr)
            
            print("✓ 進階噪音減少完成")
            return y_filtered
            
        except Exception as e:
            print(f"✗ 噪音減少失敗: {e}")
            return y
    
    def remove_ring_tones(self, y, sr):
        """檢測和去除鈴聲"""
        try:
            # 鈴聲通常在特定頻率範圍，使用帶阻濾波器
            nyquist = sr / 2
            
            # 常見鈴聲頻率範圍
            ring_frequencies = [
                (400, 500),   # 低頻鈴聲
                (800, 1000),  # 中頻鈴聲  
                (1400, 1600), # 高頻鈴聲
                (2000, 2200)  # 超高頻鈴聲
            ]
            
            y_filtered = y.copy()
            
            for low_freq, high_freq in ring_frequencies:
                if high_freq < nyquist:
                    # 創建帶阻濾波器
                    sos = signal.butter(4, [low_freq, high_freq], 
                                      btype='bandstop', fs=sr, output='sos')
                    y_filtered = signal.sosfilt(sos, y_filtered)
            
            print("✓ 鈴聲去除完成")
            return y_filtered
            
        except Exception as e:
            print(f"✗ 鈴聲去除失敗: {e}")
            return y
    
    def remove_silence_segments(self, y, sr):
        """去除空白和低能量片段"""
        try:
            # 1. 使用 librosa 的 trim 功能去除開頭和結尾的靜音
            y_trimmed, _ = librosa.effects.trim(y, top_db=25)
            
            # 2. 檢測內部的靜音片段
            # 計算短時能量
            frame_length = 2048
            hop_length = 512
            
            # 分幀計算能量
            frames = librosa.util.frame(y_trimmed, frame_length=frame_length, 
                                      hop_length=hop_length)
            energy = np.sum(frames ** 2, axis=0)
            
            # 計算動態閾值
            energy_mean = np.mean(energy)
            energy_std = np.std(energy)
            threshold = energy_mean - 2 * energy_std
            
            # 標記有效音頻片段
            valid_frames = energy > threshold
            
            # 平滑處理，避免過度切割
            kernel = np.ones(10) / 10
            valid_frames_smooth = np.convolve(valid_frames.astype(float), kernel, mode='same') > 0.3
            
            # 重建音頻
            y_processed = []
            for i, is_valid in enumerate(valid_frames_smooth):
                if is_valid:
                    start_sample = i * hop_length
                    end_sample = min(start_sample + hop_length, len(y_trimmed))
                    y_processed.extend(y_trimmed[start_sample:end_sample])
            
            y_result = np.array(y_processed)
            
            print(f"✓ 空白片段去除完成，從 {len(y)/sr:.2f}秒 縮短到 {len(y_result)/sr:.2f}秒")
            return y_result
            
        except Exception as e:
            print(f"✗ 空白片段去除失敗: {e}")
            return y
    
    def apply_noise_filters(self, y, sr):
        """應用多種噪音濾波器"""
        try:
            nyquist = sr / 2
            y_filtered = y.copy()
            
            # 1. 高通濾波器 - 去除低頻噪音（如空調聲）
            if nyquist > 100:
                sos_high = signal.butter(6, 100, btype='high', fs=sr, output='sos')
                y_filtered = signal.sosfilt(sos_high, y_filtered)
            
            # 2. 帶阻濾波器 - 去除電源噪音
            power_freqs = [50, 60, 100, 120]  # 電源噪音頻率
            for freq in power_freqs:
                if freq + 2 < nyquist:
                    sos_notch = signal.butter(4, [freq-2, freq+2], 
                                            btype='bandstop', fs=sr, output='sos')
                    y_filtered = signal.sosfilt(sos_notch, y_filtered)
            
            # 3. 低通濾波器 - 去除超高頻噪音
            cutoff_freq = min(8000, nyquist * 0.9)
            sos_low = signal.butter(6, cutoff_freq, btype='low', fs=sr, output='sos')
            y_filtered = signal.sosfilt(sos_low, y_filtered)
            
            print("✓ 噪音濾波完成")
            return y_filtered
            
        except Exception as e:
            print(f"✗ 噪音濾波失敗: {e}")
            return y
    
    def extract_voice_features(self, y, sr, frame_length=2048, hop_length=512):
        """提取語音特徵用於說話者分離"""
        try:
            # 提取 MFCC 特徵
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, 
                                       n_fft=frame_length, hop_length=hop_length)
            
            # 提取基頻 (F0)
            f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                       fmin=librosa.note_to_hz('C2'), 
                                                       fmax=librosa.note_to_hz('C7'),
                                                       frame_length=frame_length)
            
            # 提取頻譜重心
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, 
                                                                 hop_length=hop_length)[0]
            
            # 提取頻譜滾降
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, 
                                                              hop_length=hop_length)[0]
            
            # 提取零交叉率
            zcr = librosa.feature.zero_crossing_rate(y, frame_length=frame_length, 
                                                   hop_length=hop_length)[0]
            
            print("✓ 語音特徵提取完成")
            return {
                'mfccs': mfccs,
                'f0': f0,
                'voiced_flag': voiced_flag,
                'spectral_centroids': spectral_centroids,
                'spectral_rolloff': spectral_rolloff,
                'zcr': zcr
            }
            
        except Exception as e:
            print(f"✗ 特徵提取失敗: {e}")
            return None
    
    def detect_voice_activity(self, y, sr, frame_length=2048, hop_length=512):
        """檢測語音活動區域"""
        try:
            # 計算短時能量
            frame_length_samples = frame_length
            hop_length_samples = hop_length
            
            # 分幀
            frames = librosa.util.frame(y, frame_length=frame_length_samples, 
                                      hop_length=hop_length_samples)
            
            # 計算每幀的能量
            energy = np.sum(frames ** 2, axis=0)
            
            # 計算能量閾值
            energy_threshold = np.percentile(energy, 30)  # 使用30%分位數作為閾值
            
            # 檢測語音活動
            voice_activity = energy > energy_threshold
            
            # 平滑處理
            kernel = np.ones(5) / 5
            voice_activity_smooth = np.convolve(voice_activity.astype(float), kernel, mode='same') > 0.5
            
            print("✓ 語音活動檢測完成")
            return voice_activity_smooth, energy
            
        except Exception as e:
            print(f"✗ 語音活動檢測失敗: {e}")
            return None, None
    
    def separate_speakers(self, y, sr, n_speakers=2):
        """分離不同說話者的語音"""
        try:
            print(f"開始分離 {n_speakers} 個說話者...")
            
            # 參數設定
            frame_length = 2048
            hop_length = 512
            
            # 檢測語音活動
            voice_activity, energy = self.detect_voice_activity(y, sr, frame_length, hop_length)
            if voice_activity is None:
                return None
            
            # 提取特徵
            features = self.extract_voice_features(y, sr, frame_length, hop_length)
            if features is None:
                return None
            
            # 只在有語音活動的幀上進行分析
            voiced_frames = voice_activity
            
            # 準備聚類特徵
            feature_matrix = []
            valid_indices = []
            
            for i in range(len(voiced_frames)):
                if voiced_frames[i] and i < features['mfccs'].shape[1]:
                    frame_features = []
                    
                    # MFCC 特徵
                    frame_features.extend(features['mfccs'][:, i])
                    
                    # 基頻特徵 (如果有效)
                    if i < len(features['f0']) and not np.isnan(features['f0'][i]):
                        frame_features.append(features['f0'][i])
                    else:
                        frame_features.append(0)
                    
                    # 其他特徵
                    if i < len(features['spectral_centroids']):
                        frame_features.append(features['spectral_centroids'][i])
                    if i < len(features['spectral_rolloff']):
                        frame_features.append(features['spectral_rolloff'][i])
                    if i < len(features['zcr']):
                        frame_features.append(features['zcr'][i])
                    
                    feature_matrix.append(frame_features)
                    valid_indices.append(i)
            
            if len(feature_matrix) < n_speakers:
                print("✗ 語音幀數不足以進行說話者分離")
                return None
            
            # 標準化特徵
            feature_matrix = np.array(feature_matrix)
            scaler = StandardScaler()
            feature_matrix_scaled = scaler.fit_transform(feature_matrix)
            
            # K-means 聚類
            kmeans = KMeans(n_clusters=n_speakers, random_state=42, n_init=10)
            speaker_labels = kmeans.fit_predict(feature_matrix_scaled)
            
            print(f"✓ 說話者分離完成，識別出 {len(np.unique(speaker_labels))} 個說話者")
            
            return {
                'speaker_labels': speaker_labels,
                'valid_indices': valid_indices,
                'voice_activity': voice_activity,
                'hop_length': hop_length
            }
            
        except Exception as e:
            print(f"✗ 說話者分離失敗: {e}")
            return None    

    def create_speaker_masks(self, y, sr, separation_result):
        """為每個說話者創建音頻遮罩"""
        try:
            speaker_labels = separation_result['speaker_labels']
            valid_indices = separation_result['valid_indices']
            voice_activity = separation_result['voice_activity']
            hop_length = separation_result['hop_length']
            
            # 創建時間軸對應
            n_frames = len(voice_activity)
            n_speakers = len(np.unique(speaker_labels))
            
            # 初始化說話者遮罩
            speaker_masks = np.zeros((n_speakers, n_frames))
            
            # 填充說話者標籤
            label_idx = 0
            for frame_idx in range(n_frames):
                if voice_activity[frame_idx] and label_idx < len(speaker_labels):
                    speaker_id = speaker_labels[label_idx]
                    speaker_masks[speaker_id, frame_idx] = 1.0
                    label_idx += 1
            
            # 平滑遮罩
            for speaker_id in range(n_speakers):
                kernel = np.ones(5) / 5
                speaker_masks[speaker_id] = np.convolve(speaker_masks[speaker_id], kernel, mode='same')
            
            print(f"✓ 創建了 {n_speakers} 個說話者遮罩")
            return speaker_masks, hop_length
            
        except Exception as e:
            print(f"✗ 創建說話者遮罩失敗: {e}")
            return None, None
    
    def apply_speaker_separation(self, y, sr, speaker_masks, hop_length):
        """應用說話者遮罩分離音頻"""
        try:
            # 計算 STFT
            D = librosa.stft(y, hop_length=hop_length)
            magnitude, phase = np.abs(D), np.angle(D)
            
            separated_audios = []
            n_speakers = speaker_masks.shape[0]
            
            for speaker_id in range(n_speakers):
                # 調整遮罩大小以匹配 STFT
                mask = speaker_masks[speaker_id]
                if len(mask) != magnitude.shape[1]:
                    # 重新採樣遮罩以匹配 STFT 幀數
                    mask = np.interp(np.linspace(0, len(mask)-1, magnitude.shape[1]), 
                                   np.arange(len(mask)), mask)
                
                # 應用遮罩
                masked_magnitude = magnitude * mask[np.newaxis, :]
                
                # 重建音頻
                masked_stft = masked_magnitude * np.exp(1j * phase)
                separated_audio = librosa.istft(masked_stft, hop_length=hop_length, length=len(y))
                
                separated_audios.append(separated_audio)
            
            print(f"✓ 分離出 {len(separated_audios)} 個說話者的音頻")
            return separated_audios
            
        except Exception as e:
            print(f"✗ 音頻分離失敗: {e}")
            return None
    
    def enhance_speech_clarity(self, y, sr):
        """增強語音清晰度，避免模糊"""
        try:
            # 1. 輕微的預加重
            pre_emphasis = 0.97
            y_preemph = np.append(y[0], y[1:] - pre_emphasis * y[:-1])
            
            # 2. 動態範圍壓縮（輕微）
            y_compressed = np.sign(y_preemph) * np.power(np.abs(y_preemph), 0.8)
            
            # 3. 高頻增強（針對語音清晰度）
            # 設計一個輕微的高頻增強濾波器
            nyquist = sr / 2
            high_freq = min(4000, nyquist * 0.8)  # 增強 4kHz 以下的高頻
            
            # 創建一個輕微的高頻增強濾波器
            b, a = signal.butter(2, [1000, high_freq], btype='band', fs=sr)
            high_freq_component = signal.filtfilt(b, a, y_compressed)
            
            # 混合原始信號和高頻增強
            y_enhanced = y_compressed + 0.1 * high_freq_component
            
            # 4. 正規化，避免削波
            max_val = np.max(np.abs(y_enhanced))
            if max_val > 0:
                y_enhanced = y_enhanced / max_val * 0.95
            
            print("✓ 語音清晰度增強完成")
            return y_enhanced
            
        except Exception as e:
            print(f"✗ 語音增強失敗: {e}")
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
        """主要處理流程"""
        print(f"🎵 開始進階音頻處理 - 分離 {n_speakers} 個說話者")
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
        
        # 3. 進階噪音減少（去除鈴聲和空白片段）
        y_clean = self.advanced_noise_reduction(y, sr)
        
        # 4. 說話者分離
        separation_result = self.separate_speakers(y_clean, sr, n_speakers)
        if separation_result is None:
            print("⚠️ 說話者分離失敗，將保存整體去噪音頻")
            enhanced_audio = self.enhance_speech_clarity(y_clean, sr)
            self.save_audio(y, sr, "01_original.wav")
            self.save_audio(enhanced_audio, sr, "02_enhanced_speech.wav")
            return True
        
        # 5. 創建說話者遮罩
        speaker_masks, hop_length = self.create_speaker_masks(y_clean, sr, separation_result)
        if speaker_masks is None:
            return False
        
        # 6. 分離說話者音頻
        separated_audios = self.apply_speaker_separation(y_clean, sr, speaker_masks, hop_length)
        if separated_audios is None:
            return False
        
        # 7. 增強每個說話者的語音清晰度
        enhanced_speakers = []
        for i, speaker_audio in enumerate(separated_audios):
            enhanced = self.enhance_speech_clarity(speaker_audio, sr)
            enhanced_speakers.append(enhanced)
        
        # 8. 儲存結果
        results = {}
        results['original'] = self.save_audio(y, sr, "01_original.wav")
        results['cleaned'] = self.save_audio(y_clean, sr, "02_noise_reduced.wav")
        
        # 儲存每個說話者的音頻
        for i, (raw_audio, enhanced_audio) in enumerate(zip(separated_audios, enhanced_speakers)):
            speaker_num = i + 1
            results[f'speaker_{speaker_num}_raw'] = self.save_audio(
                raw_audio, sr, f"03_speaker_{speaker_num}_raw.wav"
            )
            results[f'speaker_{speaker_num}_enhanced'] = self.save_audio(
                enhanced_audio, sr, f"04_speaker_{speaker_num}_enhanced.wav"
            )
        
        # 創建混合的增強版本
        if len(enhanced_speakers) >= 2:
            mixed_enhanced = np.zeros_like(enhanced_speakers[0])
            for enhanced in enhanced_speakers:
                mixed_enhanced += enhanced
            mixed_enhanced = mixed_enhanced / len(enhanced_speakers)
            results['mixed_enhanced'] = self.save_audio(
                mixed_enhanced, sr, "05_all_speakers_enhanced.wav"
            )
        
        print("\n" + "=" * 60)
        print("🎉 處理完成！輸出檔案:")
        for key, path in results.items():
            if path:
                print(f"  📁 {key}: {Path(path).name}")
        
        print(f"\n💡 建議使用:")
        print(f"  🎯 說話者1: 04_speaker_1_enhanced.wav")
        print(f"  🎯 說話者2: 04_speaker_2_enhanced.wav")
        print(f"  🎯 整體增強: 05_all_speakers_enhanced.wav")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='進階音頻人聲分離和說話者分離工具')
    parser.add_argument('input_file', help='輸入音頻檔案路徑')
    parser.add_argument('--speakers', type=int, default=2, help='說話者數量 (預設: 2)')
    parser.add_argument('--output-dir', help='輸出目錄 (可選)')
    
    args = parser.parse_args()
    
    # 檢查輸入檔案是否存在
    if not os.path.exists(args.input_file):
        print(f"✗ 檔案不存在: {args.input_file}")
        sys.exit(1)
    
    # 創建處理器
    separator = AdvancedVoiceSeparator(args.input_file)
    
    # 如果指定了輸出目錄，則使用它
    if args.output_dir:
        separator.output_dir = Path(args.output_dir)
        separator.output_dir.mkdir(exist_ok=True)
    
    # 處理音頻
    success = separator.process_audio(n_speakers=args.speakers)
    
    if success:
        print("\n🎉 音頻處理成功完成！")
    else:
        print("\n❌ 音頻處理失敗")
        sys.exit(1)

if __name__ == "__main__":
    # 如果直接運行，處理指定的檔案
    if len(sys.argv) == 1:
        # 預設處理指定的檔案
        input_file = r"D:\python\Flask-AICares\TTS\03041966.m4a"
        if os.path.exists(input_file):
            separator = AdvancedVoiceSeparator(input_file)
            separator.process_audio(n_speakers=2)
        else:
            print(f"✗ 預設檔案不存在: {input_file}")
            print("使用方法: python advanced_voice_separation.py <音頻檔案路徑> [--speakers 2]")
    else:
        main()