# Validation Scripts

## Purpose

This directory contains scripts for validating data integrity, checking system status, and verifying configurations.

## Contents

### Audio Validation

- **check_audio_files.py**: Validate audio file integrity
- **voice_dataset_validation_system.py**: Comprehensive voice dataset validation
- **dataset_validation_dashboard.py**: Validation dashboard interface

### Data Validation

- **check_emotion_methods.py**: Validate emotion recognition methods
- **check_social_worker_names.py**: Verify social worker name data
- **final_tag_validation.py**: Final tag validation checks
- **batch_validation_processor.py**: Batch validation processing

### Query Validation

- **talent_assessment_query_validator.py**: Validate talent assessment queries

## Usage

Run validation scripts from the project root:

```bash
python scripts/validation/check_audio_files.py
```

## Related Directories

- `data/databases/` - Databases to validate
- `assets/audio/` - Audio files to validate
- `data/logs/` - Validation logs
