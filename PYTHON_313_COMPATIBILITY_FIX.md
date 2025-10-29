# Python 3.13 Compatibility Fix

## Problem
Your Flask AI customer service application was failing to start with Python 3.13 due to a missing `audioop` module that `pydub` depends on. Python 3.13 removed the `audioop` module, causing this import error:

```
ModuleNotFoundError: No module named 'audioop'
```

## Solution Applied
I've modified the `services/speech.py` file to remove the dependency on `pydub` and use `ffmpeg` directly for audio processing. This makes the application compatible with Python 3.13.

### Changes Made:

1. **Removed pydub import**: Replaced `from pydub import AudioSegment` with direct ffmpeg usage
2. **Added `convert_audio_to_wav()` function**: Uses ffmpeg to convert audio formats instead of pydub
3. **Updated `transcribe_audio()` function**: Now uses ffmpeg for audio conversion before speech recognition
4. **Updated `get_audio_duration()` function**: Uses ffprobe instead of pydub to get audio duration

### Key Features:
- ✅ **Python 3.13 Compatible**: No longer depends on the removed `audioop` module
- ✅ **Uses Local FFmpeg**: Leverages the ffmpeg binaries in your `./ffmpeg/` directory
- ✅ **Fallback Support**: Falls back to system ffmpeg if local binaries aren't found
- ✅ **Same Functionality**: Maintains all original audio processing capabilities
- ✅ **Error Handling**: Proper cleanup of temporary files and error recovery

## How It Works

### Audio Conversion Process:
1. Receives audio data in any format
2. Saves to temporary file
3. Uses ffmpeg to convert to WAV format (16kHz, mono)
4. Returns converted audio data
5. Cleans up temporary files

### Speech Recognition:
- Still uses Google Speech Recognition API
- Audio is pre-processed with ffmpeg instead of pydub
- Maintains Chinese language support (zh-TW)

### Duration Detection:
- Uses ffprobe (part of ffmpeg) to get audio duration
- More reliable than pydub for various audio formats

## Testing
Your application should now start successfully with Python 3.13. The speech recognition and audio processing features will work the same as before.

## Dependencies
- Requires ffmpeg/ffprobe (already included in your `./ffmpeg/` directory)
- SpeechRecognition library (already installed)
- No longer requires pydub for basic functionality

## Fallback Behavior
If ffmpeg is not available, the system will:
- Return original audio data without conversion
- Provide error messages for duration detection
- Still attempt speech recognition with original audio

This fix ensures your AI customer service system works seamlessly with Python 3.13 while maintaining all existing functionality.