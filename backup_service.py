# #!/usr/bin/env python3

# import os
# import time
# import tarfile
# from datetime import datetime

# SCHEDULES_FILE = "backup_schedules.txt"
# LOG_FILE = "./logs/backup_service.log"
# BACKUPS_DIR = "./backups"
# SLEEP_SECONDS = 45


# def ensure_dirs():
#     os.makedirs("./logs", exist_ok=True)
#     os.makedirs(BACKUPS_DIR, exist_ok=True)


# def log(message):
#     ensure_dirs()
#     timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M]")
#     entry = f"{timestamp} {message}"
#     with open(LOG_FILE, "a") as f:
#         f.write(entry + "\n")


# def read_schedules():
#     try:
#         with open(SCHEDULES_FILE, "r") as f:
#             return [line.rstrip("\n") for line in f if line.strip()]
#     except FileNotFoundError:
#         return []


# def write_schedules(schedules):
#     with open(SCHEDULES_FILE, "w") as f:
#         for s in schedules:
#             f.write(s + "\n")


# def create_backup(source_path, backup_name):
#     ensure_dirs()
#     tar_path = os.path.join(BACKUPS_DIR, f"{backup_name}.tar")
#     with tarfile.open(tar_path, "w") as tar:
#         tar.add(source_path, arcname=os.path.basename(source_path))
#     return tar_path


# def run():
#     ensure_dirs()
#     while True:
#         now = datetime.now()
#         current_time = now.strftime("%H:%M")

#         schedules = read_schedules()
#         remaining = []

#         for entry in schedules:
#             parts = entry.split(";")
#             if len(parts) != 3:
#                 remaining.append(entry)
#                 continue

#             source_path, scheduled_time, backup_name = parts

#             if scheduled_time == current_time:
#                 try:
#                     tar_path = create_backup(source_path, backup_name)
#                     log(f"Backup done for {source_path} in {tar_path}")
#                 except Exception as e:
#                     log(f"Error: backup failed for {source_path}: {e}")
#                     remaining.append(entry)
#             else:
#                 remaining.append(entry)

#         write_schedules(remaining)
#         time.sleep(SLEEP_SECONDS)


# if __name__ == "__main__":
#     run()