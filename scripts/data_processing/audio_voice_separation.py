#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音頻人聲分離和噪音去除工具
支援多種音頻格式，包括 m4a, wav, mp3 等
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
import noisereduce as nr
from pydub import AudioSegment
import argparse
from pathlib import Path

class VoiceSeparator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_dir = Path(input_file).parent / "separated_audio"
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_to_wav(self):
        """將 m4a 或其他格式轉換為 wav"""
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
    
    def separate_vocals(self, y, sr):
        """使用 librosa 進行人聲分離"""
        try:
            # 使用 HPSS (Harmonic-Percussive Source Separation)
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            
            # 使用 vocal separation
            S_full, phase = librosa.magphase(librosa.stft(y))
            S_filter = librosa.decompose.nn_filter(S_full,
                                                 aggregate=np.median,
                                                 metric='cosine',
                                                 width=int(librosa.time_to_frames(2, sr=sr)))
            S_filter = np.minimum(S_full, S_filter)
            
            margin_i, margin_v = 2, 10
            power = 2
            
            mask_i = librosa.util.softmask(S_filter,
                                         margin_i * (S_full - S_filter),
                                         power=power)
            
            mask_v = librosa.util.softmask(S_full - S_filter,
                                         margin_v * S_filter,
                                         power=power)
            
            # 分離人聲和背景音樂
            S_foreground = mask_v * S_full
            S_background = mask_i * S_full
            
            # 重建音頻
            vocals = librosa.istft(S_foreground * phase, length=len(y))
            background = librosa.istft(S_background * phase, length=len(y))
            
            print("✓ 人聲分離完成")
            return vocals, background, y_harmonic, y_percussive
            
        except Exception as e:
            print(f"✗ 人聲分離失敗: {e}")
            return None, None, None, None 
   
    def reduce_noise(self, y, sr):
        """去除背景噪音（鍵盤聲、鈴聲等）"""
        try:
            # 使用 noisereduce 庫進行噪音減少
            reduced_noise = nr.reduce_noise(y=y, sr=sr, stationary=True, prop_decrease=0.8)
            
            # 使用 spectral gating 進一步去除噪音
            reduced_noise = nr.reduce_noise(y=reduced_noise, sr=sr, stationary=False, prop_decrease=0.6)
            
            print("✓ 噪音減少完成")
            return reduced_noise
            
        except Exception as e:
            print(f"✗ 噪音減少失敗: {e}")
            return y
    
    def apply_filters(self, y, sr):
        """應用音頻濾波器去除特定頻率的噪音"""
        try:
            # 高通濾波器 - 去除低頻噪音
            sos_high = signal.butter(5, 80, btype='high', fs=sr, output='sos')
            y_filtered = signal.sosfilt(sos_high, y)
            
            # 帶阻濾波器 - 去除特定頻率的噪音（如電源噪音 50/60Hz）
            sos_notch = signal.butter(4, [48, 52], btype='bandstop', fs=sr, output='sos')
            y_filtered = signal.sosfilt(sos_notch, y_filtered)
            
            # 低通濾波器 - 去除高頻噪音（確保截止頻率小於奈奎斯特頻率）
            nyquist = sr / 2
            low_cutoff = min(8000, nyquist * 0.9)  # 使用較小的值
            sos_low = signal.butter(5, low_cutoff, btype='low', fs=sr, output='sos')
            y_filtered = signal.sosfilt(sos_low, y_filtered)
            
            print("✓ 濾波器處理完成")
            return y_filtered
            
        except Exception as e:
            print(f"✗ 濾波器處理失敗: {e}")
            return y
    
    def enhance_voice(self, vocals, sr):
        """增強人聲品質"""
        try:
            # 正規化音量
            vocals = librosa.util.normalize(vocals)
            
            # 動態範圍壓縮
            vocals = np.tanh(vocals * 2) * 0.8
            
            # 去除靜音部分
            vocals, _ = librosa.effects.trim(vocals, top_db=20)
            
            print("✓ 人聲增強完成")
            return vocals
            
        except Exception as e:
            print(f"✗ 人聲增強失敗: {e}")
            return vocals
    
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
        """主要處理流程"""
        print(f"開始處理音頻檔案: {self.input_file}")
        print("=" * 50)
        
        # 1. 轉換格式
        wav_file = self.convert_to_wav()
        if not wav_file:
            return False
        
        # 2. 載入音頻
        y, sr = self.load_audio(wav_file)
        if y is None:
            return False
        
        # 3. 人聲分離
        vocals, background, harmonic, percussive = self.separate_vocals(y, sr)
        if vocals is None:
            return False
        
        # 4. 噪音減少
        vocals_clean = self.reduce_noise(vocals, sr)
        
        # 5. 應用濾波器
        vocals_filtered = self.apply_filters(vocals_clean, sr)
        
        # 6. 增強人聲
        vocals_enhanced = self.enhance_voice(vocals_filtered, sr)
        
        # 7. 儲存結果
        results = {}
        results['original'] = self.save_audio(y, sr, "01_original.wav")
        results['vocals_raw'] = self.save_audio(vocals, sr, "02_vocals_raw.wav")
        results['vocals_clean'] = self.save_audio(vocals_clean, sr, "03_vocals_noise_reduced.wav")
        results['vocals_filtered'] = self.save_audio(vocals_filtered, sr, "04_vocals_filtered.wav")
        results['vocals_final'] = self.save_audio(vocals_enhanced, sr, "05_vocals_final_enhanced.wav")
        results['background'] = self.save_audio(background, sr, "06_background_music.wav")
        results['harmonic'] = self.save_audio(harmonic, sr, "07_harmonic_component.wav")
        results['percussive'] = self.save_audio(percussive, sr, "08_percussive_component.wav")
        
        print("\n" + "=" * 50)
        print("處理完成！輸出檔案:")
        for key, path in results.items():
            if path:
                print(f"  {key}: {path}")
        
        print(f"\n建議使用: {results['vocals_final']} (最終增強版人聲)")
        return True

def main():
    parser = argparse.ArgumentParser(description='音頻人聲分離和噪音去除工具')
    parser.add_argument('input_file', help='輸入音頻檔案路徑')
    parser.add_argument('--output-dir', help='輸出目錄 (可選)')
    
    args = parser.parse_args()
    
    # 檢查輸入檔案是否存在
    if not os.path.exists(args.input_file):
        print(f"✗ 檔案不存在: {args.input_file}")
        sys.exit(1)
    
    # 創建處理器
    separator = VoiceSeparator(args.input_file)
    
    # 如果指定了輸出目錄，則使用它
    if args.output_dir:
        separator.output_dir = Path(args.output_dir)
        separator.output_dir.mkdir(exist_ok=True)
    
    # 處理音頻
    success = separator.process_audio()
    
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
            separator = VoiceSeparator(input_file)
            separator.process_audio()
        else:
            print(f"✗ 預設檔案不存在: {input_file}")
            print("使用方法: python audio_voice_separation.py <音頻檔案路徑>")
    else:
        main()