# Requirements Directory

## Purpose

This directory contains all Python dependency configuration files for different deployment scenarios and feature sets.

## Contents

- `base.txt` - Core dependencies required for basic application functionality
- `voice.txt` - Voice processing and TTS dependencies
- `asr.txt` - Automatic Speech Recognition (ASR) dependencies
- `carbon.txt` - Carbon tracking system dependencies
- `full.txt` - Complete set of all dependencies
- `minimal.txt` - Minimal dependencies for lightweight deployment

## Usage

Install dependencies based on your deployment needs:

```bash
# Basic installation
pip install -r config/requirements/base.txt

# Voice processing features
pip install -r config/requirements/voice.txt

# ASR features
pip install -r config/requirements/asr.txt

# Carbon tracking only
pip install -r config/requirements/carbon.txt

# Full installation (all features)
pip install -r config/requirements/full.txt

# Minimal installation
pip install -r config/requirements/minimal.txt
```

## Related Directories

- `/services/` - Service implementations that use these dependencies
- `/config/deployment/` - Deployment configurations that reference these files
