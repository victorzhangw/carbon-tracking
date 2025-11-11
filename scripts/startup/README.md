# Startup Scripts

## Purpose

This directory contains batch scripts for starting various services and components of the system.

## Contents

### Service Startup

- **start_carbon_tracking.bat**: Start carbon tracking system
- **start-gpt-sovits.bat**: Start GPT-SoVITS service
- **start-voice-api.bat**: Start voice API service
- **start-voice-clone-service.bat**: Start voice cloning service

### Setup Scripts

- **setup-voice-system.bat**: Setup voice processing system
- **install-gpt-sovits.bat**: Install GPT-SoVITS dependencies

### Testing

- **test_pwa_features.bat**: Test PWA features

## Usage

Run batch scripts from the project root on Windows:

```cmd
scripts\startup\start_carbon_tracking.bat
```

## Notes

- These scripts are Windows-specific (.bat files)
- Ensure all dependencies are installed before running
- Check paths in scripts match your environment

## Related Directories

- `config/requirements/` - Dependency requirements
- `services/` - Services being started
- `modules/` - Modules being initialized
