#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然音頻人聲分離工具
保持人聲自然度，避免音調變化和不連續問題
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

class NaturalVoiceSeparator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_dir = Path(input_file).parent / "natural_separated_audio"
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_to_wav(self):
        """將 m4a 或其他格式轉換為 wav，保持原始品質"""
        try:
            audio = AudioSegment.from_file(self.input_file)
            # 保持原始採樣率，不強制提升
            wav_path = self.output_dir / f"{Path(self.input_file).stem}_converted.wav"
            audio.export(wav_path, format="wav")
            print(f"✓ 音頻已轉換為 WAV 格式: {wav_path}")
            return str(wav_path)
        except Exception as e:
            print(f"✗ 轉換失敗: {e}")
            return None
    
    def load_audio(self, file_path):
        """載入音頻檔案，保持原始採樣率"""
        try:
            y, sr = librosa.load(file_path, sr=None)
            print(f"✓ 音頻載入成功 - 採樣率: {sr}Hz, 長度: {len(y)/sr:.2f}秒")
            return y, sr
        except Exception as e:
            print(f"✗ 音頻載入失敗: {e}")
            return None, None
    
    def gentle_targeted_noise_reduction(self, y, sr):
        """溫和且有針對性的噪音減少，保持人聲自然度"""
        try:
            print("開始溫和的目標噪音處理...")
            
            # 1. 非常溫和的整體噪音減少
            y_stage1 = nr.reduce_noise(
                y=y, 
                sr=sr, 
                stationary=True, 
                prop_decrease=0.2,  # 非常溫和
                n_std_thresh_stationary=2.0,  # 高閾值，保護語音
                n_fft=512  # 較小窗口，保持時間解析度
            )
            
            # 2. 只針對特定頻率的鈴聲進行處理
            y_no_ring = self.remove_specific_ring_tones(y_stage1, sr)
            
            # 3. 保持連續性的輕微平滑
            y_smoothed = self.gentle_smoothing(y_no_ring, sr)
            
            print("✓ 溫和噪音處理完成")
            return y_smoothed
            
        except Exception as e:
            print(f"✗ 噪音減少失敗: {e}")
            return y
    
    def remove_specific_ring_tones(self, y, sr):
        """只去除特定的鈴聲頻率，保持語音完整"""
        try:
            nyquist = sr / 2
            y_filtered = y.copy()
            
            # 只針對最明顯的鈴聲頻率，使用很窄的帶阻濾波器
            specific_ring_freqs = [
                (440, 460),   # 標準鈴聲 A4 附近
                (880, 900),   # 高頻鈴聲
            ]
            
            for low_freq, high_freq in specific_ring_freqs:
                if high_freq < nyquist:
                    # 使用較低階數的濾波器，減少相位失真
                    sos = signal.butter(2, [low_freq, high_freq], 
                                      btype='bandstop', fs=sr, output='sos')
                    y_filtered = signal.sosfilt(sos, y_filtered)
            
            print("✓ 特定鈴聲頻率處理完成")
            return y_filtered
            
        except Exception as e:
            print(f"✗ 鈴聲處理失敗: {e}")
            return y
    
    def gentle_smoothing(self, y, sr):
        """輕微平滑處理，保持自然度"""
        try:
            # 使用很小的移動平均窗口進行輕微平滑
            window_size = int(sr * 0.001)  # 1ms 窗口
            if window_size > 1:
                kernel = np.ones(window_size) / window_size
                y_smoothed = np.convolve(y, kernel, mode='same')
            else:
                y_smoothed = y
            
            # 混合原始信號和平滑信號，保持自然度
            y_result = 0.9 * y + 0.1 * y_smoothed
            
            print("✓ 輕微平滑處理完成")
            return y_result
            
        except Exception as e:
            print(f"✗ 平滑處理失敗: {e}")
            return y    

    def extract_voice_features_gentle(self, y, sr, frame_length=1024, hop_length=256):
        """溫和的語音特徵提取，使用較小的窗口保持連續性"""
        try:
            # 使用較小的窗口和跳躍長度，保持時間連續性
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, 
                                       n_fft=frame_length, hop_length=hop_length)
            
            # 基頻提取，使用較寬鬆的參數
            f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                                       fmin=librosa.note_to_hz('C2'), 
                                                       fmax=librosa.note_to_hz('C7'),
                                                       frame_length=frame_length)
            
            # 其他特徵
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, 
                                                                 hop_length=hop_length)[0]
            zcr = librosa.feature.zero_crossing_rate(y, frame_length=frame_length, 
                                                   hop_length=hop_length)[0]
            
            print("✓ 溫和語音特徵提取完成")
            return {
                'mfccs': mfccs,
                'f0': f0,
                'voiced_flag': voiced_flag,
                'spectral_centroids': spectral_centroids,
                'zcr': zcr
            }
            
        except Exception as e:
            print(f"✗ 特徵提取失敗: {e}")
            return None
    
    def detect_voice_activity_conservative(self, y, sr, frame_length=1024, hop_length=256):
        """保守的語音活動檢測，避免過度切割"""
        try:
            # 分幀
            frames = librosa.util.frame(y, frame_length=frame_length, 
                                      hop_length=hop_length)
            
            # 計算每幀的能量
            energy = np.sum(frames ** 2, axis=0)
            
            # 使用較低的閾值，保留更多語音
            energy_threshold = np.percentile(energy, 15)  # 降低到15%分位數
            
            # 檢測語音活動
            voice_activity = energy > energy_threshold
            
            # 更強的平滑處理，避免不連續
            kernel = np.ones(15) / 15  # 增加平滑窗口
            voice_activity_smooth = np.convolve(voice_activity.astype(float), kernel, mode='same') > 0.3
            
            print("✓ 保守語音活動檢測完成")
            return voice_activity_smooth, energy
            
        except Exception as e:
            print(f"✗ 語音活動檢測失敗: {e}")
            return None, None
    
    def separate_speakers_gentle(self, y, sr, n_speakers=2):
        """溫和的說話者分離，保持連續性"""
        try:
            print(f"開始溫和分離 {n_speakers} 個說話者...")
            
            # 使用較小的窗口參數
            frame_length = 1024
            hop_length = 256
            
            # 保守的語音活動檢測
            voice_activity, energy = self.detect_voice_activity_conservative(y, sr, frame_length, hop_length)
            if voice_activity is None:
                return None
            
            # 溫和的特徵提取
            features = self.extract_voice_features_gentle(y, sr, frame_length, hop_length)
            if features is None:
                return None
            
            # 準備聚類特徵，只使用最穩定的特徵
            feature_matrix = []
            valid_indices = []
            
            for i in range(len(voice_activity)):
                if voice_activity[i] and i < features['mfccs'].shape[1]:
                    frame_features = []
                    
                    # 只使用前8個MFCC係數，避免過度細節
                    frame_features.extend(features['mfccs'][:8, i])
                    
                    # 基頻特徵 (如果有效)
                    if i < len(features['f0']) and not np.isnan(features['f0'][i]):
                        frame_features.append(features['f0'][i])
                    else:
                        frame_features.append(0)
                    
                    feature_matrix.append(frame_features)
                    valid_indices.append(i)
            
            if len(feature_matrix) < n_speakers:
                print("✗ 語音幀數不足以進行說話者分離")
                return None
            
            # 標準化特徵
            feature_matrix = np.array(feature_matrix)
            scaler = StandardScaler()
            feature_matrix_scaled = scaler.fit_transform(feature_matrix)
            
            # K-means 聚類，使用更多初始化嘗試
            kmeans = KMeans(n_clusters=n_speakers, random_state=42, n_init=20)
            speaker_labels = kmeans.fit_predict(feature_matrix_scaled)
            
            print(f"✓ 溫和說話者分離完成，識別出 {len(np.unique(speaker_labels))} 個說話者")
            
            return {
                'speaker_labels': speaker_labels,
                'valid_indices': valid_indices,
                'voice_activity': voice_activity,
                'hop_length': hop_length
            }
            
        except Exception as e:
            print(f"✗ 說話者分離失敗: {e}")
            return None
    
    def create_smooth_speaker_masks(self, y, sr, separation_result):
        """創建平滑的說話者遮罩，避免不連續"""
        try:
            speaker_labels = separation_result['speaker_labels']
            valid_indices = separation_result['valid_indices']
            voice_activity = separation_result['voice_activity']
            hop_length = separation_result['hop_length']
            
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
            
            # 強力平滑遮罩，避免突兀切換
            for speaker_id in range(n_speakers):
                # 使用較大的平滑窗口
                kernel = np.ones(21) / 21  # 增加到21點
                speaker_masks[speaker_id] = np.convolve(speaker_masks[speaker_id], kernel, mode='same')
                
                # 應用 sigmoid 函數使過渡更平滑
                speaker_masks[speaker_id] = 1 / (1 + np.exp(-10 * (speaker_masks[speaker_id] - 0.5)))
            
            print(f"✓ 創建了 {n_speakers} 個平滑說話者遮罩")
            return speaker_masks, hop_length
            
        except Exception as e:
            print(f"✗ 創建說話者遮罩失敗: {e}")
            return None, None
    
    def apply_gentle_speaker_separation(self, y, sr, speaker_masks, hop_length):
        """溫和應用說話者分離，保持自然度"""
        try:
            # 計算 STFT，使用較小的窗口
            D = librosa.stft(y, hop_length=hop_length, n_fft=1024)
            magnitude, phase = np.abs(D), np.angle(D)
            
            separated_audios = []
            n_speakers = speaker_masks.shape[0]
            
            for speaker_id in range(n_speakers):
                # 調整遮罩大小
                mask = speaker_masks[speaker_id]
                if len(mask) != magnitude.shape[1]:
                    mask = np.interp(np.linspace(0, len(mask)-1, magnitude.shape[1]), 
                                   np.arange(len(mask)), mask)
                
                # 確保遮罩不會完全為0，保持一些背景
                mask = np.maximum(mask, 0.1)  # 最小保留10%
                
                # 應用遮罩
                masked_magnitude = magnitude * mask[np.newaxis, :]
                
                # 重建音頻
                masked_stft = masked_magnitude * np.exp(1j * phase)
                separated_audio = librosa.istft(masked_stft, hop_length=hop_length, length=len(y))
                
                separated_audios.append(separated_audio)
            
            print(f"✓ 溫和分離出 {len(separated_audios)} 個說話者的音頻")
            return separated_audios
            
        except Exception as e:
            print(f"✗ 音頻分離失敗: {e}")
            return None   
 
    def natural_speech_enhancement(self, y, sr):
        """自然的語音增強，避免音調變化"""
        try:
            # 1. 非常輕微的正規化
            max_val = np.max(np.abs(y))
            if max_val > 0:
                y_normalized = y / max_val * 0.98  # 輕微正規化
            else:
                y_normalized = y
            
            # 2. 去除直流偏移
            y_dc_removed = y_normalized - np.mean(y_normalized)
            
            # 3. 非常輕微的動態範圍調整
            y_enhanced = np.sign(y_dc_removed) * np.power(np.abs(y_dc_removed), 0.95)
            
            print("✓ 自然語音增強完成")
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
        """主要處理流程 - 保持自然度優先"""
        print(f"🎵 開始自然音頻處理 - 分離 {n_speakers} 個說話者")
        print("🌟 優先保持語音自然度和連續性")
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
        
        # 3. 溫和的目標噪音減少
        y_clean = self.gentle_targeted_noise_reduction(y, sr)
        
        # 4. 自然語音增強
        y_enhanced = self.natural_speech_enhancement(y_clean, sr)
        
        # 5. 說話者分離（可選）
        separation_result = self.separate_speakers_gentle(y_enhanced, sr, n_speakers)
        
        # 6. 儲存結果
        results = {}
        results['original'] = self.save_audio(y, sr, "01_original.wav")
        results['noise_reduced'] = self.save_audio(y_clean, sr, "02_gentle_noise_reduced.wav")
        results['enhanced'] = self.save_audio(y_enhanced, sr, "03_naturally_enhanced.wav")
        
        if separation_result is not None:
            # 創建平滑說話者遮罩
            speaker_masks, hop_length = self.create_smooth_speaker_masks(y_enhanced, sr, separation_result)
            if speaker_masks is not None:
                # 溫和分離說話者
                separated_audios = self.apply_gentle_speaker_separation(y_enhanced, sr, speaker_masks, hop_length)
                if separated_audios is not None:
                    # 儲存分離的說話者音頻
                    for i, speaker_audio in enumerate(separated_audios):
                        speaker_num = i + 1
                        # 對每個說話者應用自然增強
                        speaker_enhanced = self.natural_speech_enhancement(speaker_audio, sr)
                        results[f'speaker_{speaker_num}'] = self.save_audio(
                            speaker_enhanced, sr, f"04_speaker_{speaker_num}_natural.wav"
                        )
        
        print("\n" + "=" * 60)
        print("🎉 自然處理完成！輸出檔案:")
        for key, path in results.items():
            if path:
                print(f"  📁 {key}: {Path(path).name}")
        
        print(f"\n💡 推薦使用 (保持自然度):")
        print(f"  🎯 整體增強: 03_naturally_enhanced.wav")
        if 'speaker_1' in results:
            print(f"  🎯 說話者1: 04_speaker_1_natural.wav")
        if 'speaker_2' in results:
            print(f"  🎯 說話者2: 04_speaker_2_natural.wav")
        
        print(f"\n🌟 特點: 保持原始音調和連續性，避免人工感")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='自然音頻人聲分離工具')
    parser.add_argument('input_file', help='輸入音頻檔案路徑')
    parser.add_argument('--speakers', type=int, default=2, help='說話者數量 (預設: 2)')
    parser.add_argument('--output-dir', help='輸出目錄 (可選)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"✗ 檔案不存在: {args.input_file}")
        sys.exit(1)
    
    separator = NaturalVoiceSeparator(args.input_file)
    
    if args.output_dir:
        separator.output_dir = Path(args.output_dir)
        separator.output_dir.mkdir(exist_ok=True)
    
    success = separator.process_audio(n_speakers=args.speakers)
    
    if success:
        print("\n🎉 自然音頻處理成功完成！")
    else:
        print("\n❌ 音頻處理失敗")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        input_file = r"D:\python\Flask-AICares\TTS\03041966.m4a"
        if os.path.exists(input_file):
            separator = NaturalVoiceSeparator(input_file)
            separator.process_audio(n_speakers=2)
        else:
            print(f"✗ 預設檔案不存在: {input_file}")
            print("使用方法: python natural_voice_separation.py <音頻檔案路徑> [--speakers 2]")
    else:
        main()