# API Specifications Directory

## Purpose

This directory contains API specification files for external services and integrations used in the project.

## Contents

- `gpt-sovits-api.json` - GPT-SoVITS voice cloning API specification
- `f5-tts-api.json` - F5-TTS text-to-speech API specification
- `Gpt-Sovis-API.md` - Detailed documentation for GPT-SoVITS API
- `api_description.txt` - General API descriptions and notes

## Usage

These specification files are used for:

1. **API Integration** - Reference for implementing API clients
2. **Documentation** - Understanding API endpoints and parameters
3. **Testing** - Validating API requests and responses
4. **Development** - Quick reference during feature development

### Example: Using GPT-SoVITS API

```python
import json

# Load API specification
with open('config/api_specs/gpt-sovits-api.json', 'r') as f:
    api_spec = json.load(f)

# Use specification for API calls
# See Gpt-Sovis-API.md for detailed usage examples
```

## Related Directories

- `/services/` - Service implementations that consume these APIs
- `/modules/voice_processing/` - Voice processing modules using these APIs
- `/docs/technical/voice/` - Technical documentation for voice features
