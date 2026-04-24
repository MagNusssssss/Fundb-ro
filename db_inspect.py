import sqlite3
import sys

def main():
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        print('Tables:', tables)
        cur.execute("PRAGMA table_info('Fundsachen')")
        info = cur.fetchall()
        print('Fundsachen schema:', info)
        try:
            cur.execute('SELECT COUNT(*) FROM Fundsachen')
            print('Rows in Fundsachen:', cur.fetchone()[0])
        except Exception as e:
            print('SELECT COUNT error:', e)
        conn.close()
    except Exception as e:
        print('ERROR:', e)
        sys.exit(1)

if __name__ == '__main__':
    main()
