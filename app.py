import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Zugriff auf Spalten per Name möglich
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    # Alle Einträge aus der Tabelle holen
    items = conn.execute('SELECT * FROM Fundsachen').fetchall()
    conn.close()
    return render_template('index.html', einkaufsliste=items)

if __name__ == '__main__':
    app.run(debug=True)