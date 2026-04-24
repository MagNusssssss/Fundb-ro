from app import app
import sqlite3

print('Starting smoke test...')
with app.test_client() as client:
    resp = client.post('/add', data={
        'name': 'SMOKETEST_ITEM',
        'description': 'added by smoke test',
        'found_date': '2026-04-24',
        'location': 'SmokeLocation',
        'status': 'gefunden'
    }, follow_redirects=True)
    print('POST /add status code:', resp.status_code)

conn = sqlite3.connect('database.db')
cur = conn.cursor()
rows = cur.execute("SELECT id, name, found_date, location, status FROM Fundsachen WHERE name = ?", ('SMOKETEST_ITEM',)).fetchall()
print('Rows found:', rows)
conn.close()
print('Smoke test finished.')
