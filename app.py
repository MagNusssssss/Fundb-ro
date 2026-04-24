import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    items = conn.execute('SELECT * FROM Fundsachen').fetchall()
    conn.close()
    return render_template('index.html', Fundsachen=items)

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    description = request.form.get('description')
    found_date = request.form.get('found_date')
    location = request.form.get('location')
    status = request.form.get('status')

    conn = get_db_connection()
    conn.execute('INSERT INTO Fundsachen (name, description, found_date, location, status) VALUES (?, ?, ?, ?, ?)',
                 (name, description, found_date, location, status))
    conn.commit()
    conn.close()

    from flask import redirect, url_for
    return redirect(url_for('index'))