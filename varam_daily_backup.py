from pathlib import Path
from datetime import date
import sqlite3
import os

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "db.sqlite3"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

today = date.today().strftime("%Y%m%d")
backup_file = BACKUP_DIR / f"varam_daily_{today}.sqlite3"
temp_file = BACKUP_DIR / f"varam_daily_{today}.tmp"

if not DB_FILE.exists():
    raise SystemExit(f"Database not found: {DB_FILE}")

try:
    source = sqlite3.connect(str(DB_FILE))
    try:
        destination = sqlite3.connect(str(temp_file))
        try:
            source.backup(destination)
            destination.commit()
        finally:
            destination.close()
    finally:
        source.close()

    check_db = sqlite3.connect(str(temp_file))
    try:
        integrity = check_db.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]
    finally:
        check_db.close()

    if integrity != "ok":
        raise RuntimeError(f"Backup integrity failed: {integrity}")

    os.replace(temp_file, backup_file)

    daily_backups = sorted(
        BACKUP_DIR.glob("varam_daily_*.sqlite3"),
        key=lambda p: p.name,
        reverse=True,
    )

    for old_backup in daily_backups[14:]:
        old_backup.unlink()

    print("VARAM DAILY BACKUP SUCCESS")
    print(f"File: {backup_file}")
    print(f"Size: {backup_file.stat().st_size:,} bytes")
    print(f"Integrity: {integrity}")
    print(f"Daily backups retained: {min(len(daily_backups), 14)}")

finally:
    if temp_file.exists():
        try:
            temp_file.unlink()
        except PermissionError:
            print(f"Warning: Could not remove temporary file: {temp_file}")
