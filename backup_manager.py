#!/usr/bin/env python3

import sys
import os
import subprocess
import signal
from datetime import datetime

SCHEDULES_FILE = "backup_schedules.txt"
LOG_FILE = "./logs/backup_manager.log"
BACKUPS_DIR = "./backups"
SERVICE_SCRIPT = "backup_service.py"


def ensure_logs_dir():
    os.makedirs("./logs", exist_ok=True)


def log(message):
    ensure_logs_dir()
    timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M]")
    entry = f"{timestamp} {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")


def cmd_create(schedule):
    parts = schedule.split(";")
    if len(parts) != 3 or not all(parts):
        log(f"Error: malformed schedule: {schedule}")
        return
    try:
        with open(SCHEDULES_FILE, "a") as f:
            f.write(schedule + "\n")
        log(f"New schedule added: {schedule}")
    except Exception as e:
        log(f"Error: could not write schedule: {e}")

