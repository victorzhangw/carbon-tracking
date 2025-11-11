# Data Processing Scripts

## Purpose

This directory contains scripts for processing, transforming, and updating data in the system.

## Contents

### Social Worker Data Processing

- **update_social_worker_names.py**: Update social worker names in database
- **update_names_extended.py**: Extended name update functionality
- **add_more_social_workers.py**: Add new social workers to the system

### Audio Processing

- **process_03041966_audio.py**: Process specific audio file
- **process_advanced_03041966.py**: Advanced audio processing
- **process_natural_03041966.py**: Natural audio processing
- **advanced_voice_separation.py**: Advanced voice separation algorithm
- **audio_voice_separation.py**: Basic audio voice separation
- **natural_voice_separation.py**: Natural voice separation
- **optimized_natural_voice_separation.py**: Optimized natural separation
- **volume_balanced_voice_separation.py**: Volume-balanced separation

## Usage

Run scripts directly from the project root:

```bash
python scripts/data_processing/update_social_worker_names.py
```

## Related Directories

- `data/databases/` - Database files to process
- `assets/audio/` - Audio files for processing
- `modules/voice_processing/` - Voice processing modules
