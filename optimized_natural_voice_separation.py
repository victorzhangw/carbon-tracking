#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
優化的自然音頻人聲分離工具
進一步改善音調穩定性和連續性
"""

import os
import sys
import librosa
import soundfile as sf
import numpy as np
from scipy import signal
import noisereduce as nr
from pydub import AudioSegment
from pathlib import Path

class OptimizedNaturalVoiceSeparator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_dir = Path(input_file).parent / "optimized_natural_audio"
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_to_wav(self):
        """轉換為 WAV 格式，保持最佳品質"""
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
    
    def minimal_noise_reduction(self, y, sr):
        """最小化噪音處理，只去除明顯的鈴聲"""
        try:
            print("開始最小化噪音處理...")
            
            # 1. 非常輕微的整體噪音減少
            y_clean = nr.reduce_noise(
                y=y, 
                sr=sr, 
                stationary=True, 
                prop_decrease=0.1,  # 極其溫和
                n_std_thresh_stationary=2.5,  # 高閾值
                n_fft=512
            )
            
            # 2. 只針對最明顯的鈴聲頻率
            y_no_ring = self.remove_obvious_ring_tones(y_clean, sr)
            
            print("✓ 最小化噪音處理完成")
            return y_no_ring
            
        except Exception as e:
            print(f"✗ 噪音處理失敗: {e}")
            return y
    
    def remove_obvious_ring_tones(self, y, sr):
        """只去除最明顯的鈴聲，保護語音"""
        try:
            nyquist = sr / 2
            y_filtered = y.copy()
            
            # 只針對最典型的鈴聲頻率，使用極窄的帶阻
            ring_freq = 440  # 標準 A4 音調
            bandwidth = 10   # 極窄帶寬
            
            if ring_freq + bandwidth/2 < nyquist:
                low_freq = ring_freq - bandwidth/2
                high_freq = ring_freq + bandwidth/2
                
                # 使用最低階數的濾波器
                sos = signal.butter(1, [low_freq, high_freq], 
                                  btype='bandstop', fs=sr, output='sos')
                y_filtered = signal.sosfilt(sos, y_filtered)
            
            print("✓ 明顯鈴聲去除完成")
            return y_filtered
            
        except Exception as e:
            print(f"✗ 鈴聲處理失敗: {e}")
            return y
    
    def preserve_natural_characteristics(self, y, sr):
        """保持自然特性的增強"""
        try:
            # 1. 只做最基本的正規化
            max_val = np.max(np.abs(y))
            if max_val > 0.95:  # 只在需要時才正規化
                y_normalized = y / max_val * 0.95
            else:
                y_normalized = y
            
            # 2. 去除直流偏移
            y_dc_removed = y_normalized - np.mean(y_normalized)
            
            # 3. 極其輕微的平滑（幾乎不處理）
            window_size = max(1, int(sr * 0.0005))  # 0.5ms 極小窗口
            if window_size > 1:
                kernel = np.ones(window_size) / window_size
                y_smoothed = np.convolve(y_dc_removed, kernel, mode='same')
                # 只混合很少比例的平滑信號
                y_result = 0.98 * y_dc_removed + 0.02 * y_smoothed
            else:
                y_result = y_dc_removed
            
            print("✓ 自然特性保持完成")
            return y_result
            
        except Exception as e:
            print(f"✗ 自然特性處理失敗: {e}")
            return y
    
    def simple_speaker_separation(self, y, sr):
        """簡化的說話者分離，保持連續性"""
        try:
            print("開始簡化說話者分離...")
            
            # 使用更大的窗口，減少時間解析度以保持連續性
            frame_length = 4096  # 增大窗口
            hop_length = 1024    # 增大跳躍
            
            # 計算 STFT
            D = librosa.stft(y, n_fft=frame_length, hop_length=hop_length)
            magnitude, phase = np.abs(D), np.angle(D)
            
            # 使用簡單的頻率分割方法
            freq_bins = magnitude.shape[0]
            mid_freq = freq_bins // 2
            
            # 創建兩個頻率遮罩
            mask1 = np.ones_like(magnitude)
            mask2 = np.ones_like(magnitude)
            
            # 軟分割，保持重疊
            mask1[mid_freq:] *= 0.3  # 低頻為主
            mask2[:mid_freq] *= 0.3  # 高頻為主
            
            # 重建音頻
            stft1 = magnitude * mask1 * np.exp(1j * phase)
            stft2 = magnitude * mask2 * np.exp(1j * phase)
            
            speaker1 = librosa.istft(stft1, hop_length=hop_length, length=len(y))
            speaker2 = librosa.istft(stft2, hop_length=hop_length, length=len(y))
            
            print("✓ 簡化說話者分離完成")
            return [speaker1, speaker2]
            
        except Exception as e:
            print(f"✗ 說話者分離失敗: {e}")
            return None
    
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
    
    def process_audio(self):
        """優化的處理流程"""
        print("🎵 開始優化自然音頻處理")
        print("🌟 最大化保持原始特性")
        print("=" * 50)
        print(f"處理檔案: {self.input_file}")
        
        # 1. 轉換格式
        wav_file = self.convert_to_wav()
        if not wav_file:
            return False
        
        # 2. 載入音頻
        y, sr = self.load_audio(wav_file)
        if y is None:
            return False
        
        # 3. 最小化噪音處理
        y_clean = self.minimal_noise_reduction(y, sr)
        
        # 4. 保持自然特性
        y_natural = self.preserve_natural_characteristics(y_clean, sr)
        
        # 5. 簡化說話者分離
        separated_speakers = self.simple_speaker_separation(y_natural, sr)
        
        # 6. 儲存結果
        results = {}
        results['original'] = self.save_audio(y, sr, "01_original.wav")
        results['minimal_processed'] = self.save_audio(y_clean, sr, "02_minimal_noise_reduced.wav")
        results['optimized'] = self.save_audio(y_natural, sr, "03_optimized_natural.wav")
        
        if separated_speakers:
            for i, speaker_audio in enumerate(separated_speakers):
                speaker_num = i + 1
                # 對分離的音頻也應用自然特性保持
                speaker_natural = self.preserve_natural_characteristics(speaker_audio, sr)
                results[f'speaker_{speaker_num}'] = self.save_audio(
                    speaker_natural, sr, f"04_speaker_{speaker_num}_optimized.wav"
                )
        
        print("\n" + "=" * 50)
        print("🎉 優化處理完成！輸出檔案:")
        for key, path in results.items():
            if path:
                print(f"  📁 {key}: {Path(path).name}")
        
        print(f"\n💡 最佳選擇:")
        print(f"  🎯 整體優化: 03_optimized_natural.wav")
        if separated_speakers:
            print(f"  🎯 說話者分離: 04_speaker_X_optimized.wav")
        
        print(f"\n🌟 特點: 最大化保持原始音調和自然度")
        
        return True

def main():
    input_file = r"D:\python\Flask-AICares\TTS\03041966.m4a"
    
    print("🎵 優化自然音頻處理工具")
    print("=" * 50)
    print("🌟 專門優化:")
    print("  • 最大化保持原始音調")
    print("  • 極致的語音連續性")
    print("  • 最小化人工處理感")
    print("  • 只去除最明顯的噪音")
    print("=" * 50)
    
    if not os.path.exists(input_file):
        print(f"❌ 檔案不存在: {input_file}")
        return False
    
    try:
        separator = OptimizedNaturalVoiceSeparator(input_file)
        success = separator.process_audio()
        
        if success:
            print("\n🎉 優化處理完成！")
            print(f"📁 輸出目錄: {separator.output_dir}")
            print("\n💡 建議優先試聽: 03_optimized_natural.wav")
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