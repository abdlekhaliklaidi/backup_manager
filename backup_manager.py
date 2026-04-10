#!/usr/bin/env python3

import os
import sys
import subprocess
import signal
from datetime import datetime

# -------- CONFIG -------- #
LOG_DIR = "./logs"
LOG_FILE = os.path.join(LOG_DIR, "backup_manager.log")
PID_FILE = os.path.join(LOG_DIR, "backup_service.pid")
SCHEDULE_FILE = "backup_schedules.txt"
BACKUPS_DIR = "./backups"
SERVICE_SCRIPT = "backup_service.py"


# -------- UTILS -------- #
def now():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def log(msg):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(f"[{now()}] {msg}\n")
    except Exception:
        print("Error: can't write log")


def read_pid():
    try:
        if not os.path.exists(PID_FILE):
            return None
        with open(PID_FILE, "r") as f:
            return int(f.read().strip())
    except Exception:
        return None


def is_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def get_running_pid():
    pid = read_pid()
    if pid and is_running(pid):
        return pid

    # clean stale PID
    try:
        if pid:
            os.remove(PID_FILE)
    except Exception:
        pass

    return None


# -------- COMMANDS -------- #

def create(schedule):
    parts = schedule.split(";")

    if len(parts) != 3:
        log(f"Error: malformed schedule: {schedule}")
        return

    folder, time_str, name = [p.strip() for p in parts]

    if not folder or not time_str or not name:
        log(f"Error: malformed schedule: {schedule}")
        return

    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        log(f"Error: malformed schedule: {schedule}")
        return

    try:
        with open(SCHEDULE_FILE, "a") as f:
            f.write(f"{folder};{time_str};{name}\n")
        log(f"New schedule added: {folder};{time_str};{name}")
    except Exception as e:
        log(f"Error: can't write schedule: {e}")


def list_schedules():
    try:
        with open(SCHEDULE_FILE, "r") as f:
            schedules = [l.strip() for l in f if l.strip()]

        log("Show schedules list")

        for i, s in enumerate(schedules):
            print(f"{i}: {s}")

    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")


def delete(index):
    try:
        with open(SCHEDULE_FILE, "r") as f:
            schedules = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")
        return

    try:
        index = int(index)
        schedules.pop(index)
    except Exception:
        log(f"Error: can't find schedule at index {index}")
        return

    try:
        with open(SCHEDULE_FILE, "w") as f:
            for s in schedules:
                f.write(s + "\n")

        log(f"Schedule at index {index} deleted")

    except Exception as e:
        log(f"Error: can't write schedules: {e}")


def start():
    if get_running_pid():
        log("Error: backup_service already running")
        return

    try:
        proc = subprocess.Popen(
            [sys.executable, SERVICE_SCRIPT],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        with open(PID_FILE, "w") as f:
            f.write(str(proc.pid))

        log("backup_service started")

    except Exception as e:
        log(f"Error: can't start backup_service: {e}")


def stop():
    pid = get_running_pid()

    if not pid:
        log("Error: can't stop backup_service")
        return

    try:
        os.kill(pid, signal.SIGTERM)

        try:
            os.remove(PID_FILE)
        except Exception:
            pass

        log("backup_service stopped")

    except Exception as e:
        log(f"Error: can't stop backup_service: {e}")


def backups():
    if not os.path.isdir(BACKUPS_DIR):
        log("Error: can't find backups directory")
        return

    log("Show backups list")

    for f in sorted(os.listdir(BACKUPS_DIR)):
        if f.endswith(".tar"):
            print(f)


# -------- MAIN -------- #

def main():
    if len(sys.argv) < 2:
        log("Error: invalid command")
        return

    cmd = sys.argv[1]

    if cmd == "create" and len(sys.argv) == 3:
        create(sys.argv[2])

    elif cmd == "list":
        list_schedules()

    elif cmd == "delete" and len(sys.argv) == 3:
        delete(sys.argv[2])

    elif cmd == "start":
        start()

    elif cmd == "stop":
        stop()

    elif cmd == "backups":
        backups()

    else:
        log("Error: invalid command")


if __name__ == "__main__":
    main()
