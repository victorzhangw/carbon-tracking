# Database Files

## Purpose

This directory contains all SQLite database files used by the application.

## Contents

- `carbon_tracking.db` - Carbon emission tracking system database
- `customer_service.db` - Customer service and AI interaction database

## Usage

Database files are accessed by:

- `database.py` - Main database connection module
- `database_carbon_tracking.py` - Carbon tracking database module (now in `modules/carbon_tracking/`)
- Various service modules

## Configuration

Database paths are configured in:

- `config.py` - Main configuration file
- Individual database modules

## Backup

Database backups are stored in `backups/databases/` with timestamps.

## Related Directories

- `backups/databases/` - Database backup files
- `modules/carbon_tracking/` - Carbon tracking module
- `services/` - Service layer that uses databases
