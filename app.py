from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize the database (using SQLite for simplicity)
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date_added DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_due_messages():
    intervals = [3, 15, 60, 180, 360]  # days
    today = datetime.now().date()
    due_messages = []

    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages')
    messages = c.fetchall()
    conn.close()

    for message in messages:
        date_added = datetime.strptime(message[2], '%Y-%m-%d').date()
        days_since_added = (today - date_added).days
        if days_since_added in intervals:
            due_messages.append(message)

    return due_messages

# Route to display and add messages
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        date_added = datetime.now().date().isoformat()
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute('INSERT INTO messages (content, date_added) VALUES (?, ?)', (content, date_added))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages')
    messages = c.fetchall()
    conn.close()

    due_messages = get_due_messages()

    return render_template('index.html', messages=messages, due_messages=due_messages)

if __name__ == '__main__':
    app.run(debug=True)
