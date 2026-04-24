import sqlite3
import shutil
import time
import os
import sys

OLD_DB = 'database.db'
SCHEMA = 'schema.sql'
BACKUP = f"{OLD_DB}.bak.{int(time.time())}"
NEW_DB = 'database_fixed.db'

def make_backup():
    if os.path.exists(OLD_DB):
        shutil.copy2(OLD_DB, BACKUP)
        print('Backup created:', BACKUP)
    else:
        print('No existing database to backup.')

def create_new_db():
    if not os.path.exists(SCHEMA):
        print('schema.sql not found; cannot create new DB')
        sys.exit(1)
    conn = sqlite3.connect(NEW_DB)
    with open(SCHEMA, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print('Created new DB:', NEW_DB)

def try_copy_rows():
    rows_copied = 0
    try:
        old = sqlite3.connect(OLD_DB)
    except Exception as e:
        print('Could not open old DB:', e)
        return rows_copied

    try:
        old_cur = old.cursor()
        old_cur.execute("SELECT * FROM Fundsachen")
        rows = old_cur.fetchall()
        print(f'Found {len(rows)} rows in old DB (attempting to copy)')
    except Exception as e:
        print('Could not read rows from old DB:', e)
        old.close()
        return rows_copied

    new = sqlite3.connect(NEW_DB)
    new_cur = new.cursor()
    for r in rows:
        try:
            new_cur.execute('INSERT INTO Fundsachen (id, name, description, found_date, location, status) VALUES (?, ?, ?, ?, ?, ?)', r)
            rows_copied += 1
        except Exception as e:
            # try inserting without id (let sqlite autoincrement)
            try:
                new_cur.execute('INSERT INTO Fundsachen (name, description, found_date, location, status) VALUES (?, ?, ?, ?, ?)', r[1:])
                rows_copied += 1
            except Exception as e2:
                print('Failed to copy row:', r, 'errors:', e, e2)
    new.commit()
    new.close()
    old.close()
    print('Rows copied to new DB:', rows_copied)
    return rows_copied


def swap_dbs():
    # move original to backup (already done), move new into place
    try:
        if os.path.exists(OLD_DB):
            os.remove(OLD_DB)
        shutil.move(NEW_DB, OLD_DB)
        print('Replaced old DB with fixed DB; backup at', BACKUP)
    except Exception as e:
        print('Failed to swap DB files:', e)

if __name__ == '__main__':
    print('Starting DB recovery')
    make_backup()
    create_new_db()
    copied = try_copy_rows()
    if copied > 0:
        swap_dbs()
    else:
        print('No rows copied. New DB created at', NEW_DB, 'backup at', BACKUP)
    # final integrity check
    try:
        conn = sqlite3.connect(OLD_DB)
        cur = conn.cursor()
        cur.execute("PRAGMA integrity_check;")
        print('Final PRAGMA integrity_check:', cur.fetchall())
        conn.close()
    except Exception as e:
        print('Final integrity check failed:', e)
