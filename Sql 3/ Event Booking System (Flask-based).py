from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('event_booking.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        location TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return 'Welcome to the Event Booking System!'

@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form['name']
    date = request.form['date']
    location = request.form['location']

    conn = sqlite3.connect('event_booking.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (name, date, location) VALUES (?, ?, ?)', (name, date, location))
    conn.commit()
    conn.close()
    return 'Event added!'

if __name__ == '__main__':
    app.run(debug=True)
