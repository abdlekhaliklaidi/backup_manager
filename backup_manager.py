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


def cmd_list():
    try:
        with open(SCHEDULES_FILE, "r") as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]
        log("Show schedules list")
        for i, line in enumerate(lines):
            print(f"{i}: {line}")
    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")


def cmd_delete(index_str):
    try:
        index = int(index_str)
    except ValueError:
        log(f"Error: invalid index: {index_str}")
        return
    try:
        with open(SCHEDULES_FILE, "r") as f:
            lines = [l for l in f if l.strip()]
    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")
        return
    if index < 0 or index >= len(lines):
        log(f"Error: can't find schedule at index {index}")
        return
    del lines[index]
    with open(SCHEDULES_FILE, "w") as f:
        f.writelines(lines)
    log(f"Schedule at index {index} deleted")


def find_service_pid():
    try:
        result = subprocess.check_output(["ps", "-A", "-f"], text=True)
        for line in result.splitlines():
            if SERVICE_SCRIPT in line and "python" in line:
                parts = line.split()
                return int(parts[1])
    except Exception:
        pass
    return None


def cmd_start():
    pid = find_service_pid()
    if pid is not None:
        log("Error: backup_service already running")
        return
    try:
        subprocess.Popen(
            [sys.executable, SERVICE_SCRIPT],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log("backup_service started")
    except Exception as e:
        log(f"Error: could not start backup_service: {e}")


def cmd_stop():
    pid = find_service_pid()
    if pid is None:
        log("Error: can't stop backup_service")
        return
    try:
        os.kill(pid, signal.SIGTERM)
        log("backup_service stopped")
    except Exception as e:
        log(f"Error: can't stop backup_service: {e}")


def cmd_backups():
    try:
        files = os.listdir(BACKUPS_DIR)
        log("Show backups list")
        for f in files:
            print(f)
    except FileNotFoundError:
        log("Error: can't find backups directory")


def main():
    if len(sys.argv) < 2:
        log("Error: no command provided")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            log("Error: missing schedule argument")
        else:
            cmd_create(sys.argv[2])
    elif command == "list":
        cmd_list()
    elif command == "delete":
        if len(sys.argv) < 3:
            log("Error: missing index argument")
        else:
            cmd_delete(sys.argv[2])
    elif command == "start":
        cmd_start()
    elif command == "stop":
        cmd_stop()
    elif command == "backups":
        cmd_backups()
    else:
        log(f"Error: unknown command: {command}")


if __name__ == "__main__":
    main()