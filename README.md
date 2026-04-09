# Backup Manager

Backup Manager is a Python-based system that automates directory backups using a command-line interface (CLI). It allows users to schedule backups, run a background service, and keep logs of all operations.

# Project Goal

This project solves the problem of manual backups, which are:

Error-prone ❌
Time-consuming ⏳

# It replaces them with a system that is:

Automated 🤖
Scheduled ⏰
Logged 📜

# 🗂️ Project Structure

backup-manager/
├── backup_manager.py
├── backup_service.py
├── backup_schedules.txt
├── backups/
├── logs/
│   ├── backup_manager.log
│   └── backup_service.log
└── README.md

# How It Works
🔹 1. backup_manager.py

# This script is responsible for:

Creating schedules
Listing schedules
Deleting schedules
Starting and stopping the service
Listing backups

# 2. backup_service.py

This script runs in the background:

Reads scheduled tasks

Checks the current time

Executes backups when times match

Removes completed schedules

# Available Commands
# Create a Schedule
python3 backup_manager.py create "path;HH:MM;backup_name"

Example:

python3 backup_manager.py create "test;16:07;backup_test"

# List Schedules

python3 backup_manager.py list

# Start the Service

python3 backup_manager.py start

# Stop the Service

python3 backup_manager.py stop

# List Backups

python3 backup_manager.py backups

<!-- python3 backup_manager.py create "test;16:07;backup_test"
python3 backup_manager.py list
python3 backup_manager.py start
ls backups -->