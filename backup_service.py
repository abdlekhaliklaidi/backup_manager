#!/usr/bin/env python3

import os
import time
import tarfile
from datetime import datetime

SCHEDULE_FILE = "backup_schedules.txt"
LOG_DIR = "./logs"
LOG_FILE = os.path.join(LOG_DIR, "backup_service.log")
BACKUPS_DIR = "./backups"
PID_FILE = os.path.join(LOG_DIR, "backup_service.pid")
SLEEP_SECONDS = 45


def now():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def log(msg):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(f"[{now()}] {msg}\n")
    except Exception:
        pass


def read_schedules():
    try:
        with open(SCHEDULE_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        log("Error: can't read backup_schedules.txt")
        return []


def write_schedules(schedules):
    try:
        with open(SCHEDULE_FILE, "w") as f:
            for s in schedules:
                f.write(s + "\n")
    except Exception:
        log("Error: can't write backup_schedules.txt")


def create_backup(folder, name):
    if not os.path.isdir(folder):
        log(f"Error: can't find folder {folder}")
        return None

    try:
        os.makedirs(BACKUPS_DIR, exist_ok=True)
        path = os.path.join(BACKUPS_DIR, f"{name}.tar")

        with tarfile.open(path, "w") as tar:
            tar.add(folder, arcname=os.path.basename(folder))

        return path
    except Exception:
        log(f"Error: tar failed for {folder}")
        return None


def current_time():
    return datetime.now().strftime("%H:%M")


def run():
    log("backup_service starting")

    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception:
        log("Error: cannot write pid file")

    while True:
        try:
            schedules = read_schedules()
            now_time = current_time()
            remaining = []

            for entry in schedules:
                parts = entry.split(";")

                if len(parts) != 3:
                    log(f"Error: malformed schedule: {entry}")
                    continue

                folder, time_str, name = [p.strip() for p in parts]

                if time_str == now_time:
                    tar_path = create_backup(folder, name)
                    if tar_path:
                        log(f"Backup done for {folder} in {tar_path}")
                else:
                    remaining.append(entry)

            write_schedules(remaining)

        except Exception:
            log("Error: unexpected failure in loop")

        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    run()
