# Audio Assets

## Purpose

This directory contains all audio files used in the project, including mock voices, generated voices, uploaded audio, TTS outputs, and voice processing results.

## Contents

- `mockvoice/` - Mock voice samples for testing
- `genvoice/` - Generated voice outputs
- `uploads/` - User-uploaded audio files
- `tts/` - Text-to-Speech output files
- `voice_output/` - Voice processing and synthesis outputs

## Usage

Audio files in this directory are referenced by various services:

- Voice processing services (`services/voice_processing/`)
- TTS services (`services/tts.py`)
- Voice clone services (`modules/voice_processing/`)

## File Organization

- Keep audio files organized by their source/purpose in subdirectories
- Use descriptive filenames with timestamps when applicable
- Clean up temporary audio files regularly

## Related Directories

- `static/audio/` - Audio files served to frontend
- `data/logs/` - Audio processing logs
