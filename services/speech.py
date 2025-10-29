import io
import os
import tempfile

# Python 3.13 compatible audio processing without pydub
def convert_audio_to_wav(audio_data):
    """Convert audio data to WAV format using ffmpeg directly"""
    try:
        import subprocess
        
        # Create temporary input and output files
        with tempfile.NamedTemporaryFile(suffix='.audio', delete=False) as input_file:
            input_file.write(audio_data)
            input_path = input_file.name
        
        output_path = input_path + '.wav'
        
        # Use ffmpeg to convert to WAV
        ffmpeg_path = './ffmpeg/ffmpeg.exe'  # Use local ffmpeg
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = 'ffmpeg'  # Fallback to system ffmpeg
        
        cmd = [
            ffmpeg_path,
            '-i', input_path,
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',      # mono
            '-f', 'wav',
            '-y',            # overwrite output
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Read the converted WAV file
        with open(output_path, 'rb') as wav_file:
            wav_data = wav_file.read()
        
        # Clean up temporary files
        os.unlink(input_path)
        os.unlink(output_path)
        
        return wav_data
        
    except Exception as e:
        print(f"Audio conversion error: {e}")
        # Clean up on error
        try:
            if 'input_path' in locals():
                os.unlink(input_path)
            if 'output_path' in locals() and os.path.exists(output_path):
                os.unlink(output_path)
        except:
            pass
        return audio_data  # Return original data if conversion fails

# Alternative speech recognition for Python 3.13 compatibility
def transcribe_with_openai_whisper(audio_data):
    """Alternative transcription using OpenAI Whisper API"""
    import requests
    import tempfile
    import os
    
    try:
        # Convert audio to WAV format first
        wav_data = convert_audio_to_wav(audio_data)
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(wav_data)
            temp_path = temp_file.name
        
        # For now, return a placeholder - you can implement Whisper API here
        os.unlink(temp_path)
        return "語音轉文字功能暫時不可用 (Python 3.13 兼容性問題)"
        
    except Exception as e:
        return f"音頻處理錯誤: {e}"

# Try to import speech_recognition, fallback to alternative
try:
    import speech_recognition as sr
    USE_SPEECH_RECOGNITION = True
    print("✅ speech_recognition imported successfully")
except ImportError:
    print("⚠️ Warning: speech_recognition not compatible with Python 3.13, using fallback")
    USE_SPEECH_RECOGNITION = False

def transcribe_audio(audio_data):
    """使用 Google Speech Recognition 進行中文語音轉文字 (Python 3.13 compatible)"""
    if not USE_SPEECH_RECOGNITION:
        return transcribe_with_openai_whisper(audio_data)
    
    recognizer = sr.Recognizer()
    try:
        # Convert audio to WAV format using ffmpeg instead of pydub
        wav_data = convert_audio_to_wav(audio_data)
        wav_audio = io.BytesIO(wav_data)
        
        # Use speech_recognition to process audio
        with sr.AudioFile(wav_audio) as source:
            # 調整識別器參數
            recognizer.energy_threshold = 10  # 調整能量閾值
            recognizer.dynamic_energy_threshold = True  # 啟用動態能量閾值
            recognizer.pause_threshold = 0.8  # 調整停頓閾值
            
            # 錄製音頻
            audio_content = recognizer.record(source)
            
            # 使用 Google Speech Recognition 進行中文識別
            transcript = recognizer.recognize_google(
                audio_content, 
                language='zh-TW',  # 設置為繁體中文
                show_all=False    # 返回最可能的結果
            )
            return transcript
    except sr.UnknownValueError:
        return "無法識別語音內容，請說話更清晰或調整麥克風。"
    except sr.RequestError as e:
        return f"Google Speech Recognition 服務錯誤: {e}"
    except Exception as e:
        print(f"轉錄過程中發生錯誤: {e}")
        return "音頻處理過程中發生錯誤，請重試。"

def get_audio_duration(file_path):
    """獲取音頻檔案的時長（秒）- Python 3.13 compatible"""
    try:
        import subprocess
        
        ffmpeg_path = './ffmpeg/ffmpeg.exe'
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = 'ffmpeg'
        
        # Use ffprobe to get duration
        cmd = [
            ffmpeg_path.replace('ffmpeg', 'ffprobe'),
            '-v', 'quiet',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
        
    except Exception as e:
        print(f"無法獲取音頻時長: {e}")
        return 0
