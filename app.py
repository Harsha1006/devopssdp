from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to initialize the database (create table if it doesn't exist)
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create the bookings table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT, 
            phone TEXT,
            people INTEGER,
            date TEXT,
            time TEXT
        )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Initialize the database (this will create the table if it doesn't exist)
init_db()

# Home route: Display the booking form
@app.route('/')
def index():
    return render_template('index.html')

# Booking submission: Save the booking to the database
@app.route('/book', methods=['POST'])
def book():
    # Collect form data from the POST request
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    people = request.form['people']
    date = request.form['date']
    time = request.form['time']

    # Connect to the SQLite database and insert the reservation data
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO bookings (name, email, phone, people, date, time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, people, date, time))
    conn.commit()
    conn.close()

    # Redirect to success page after the booking is made
    return redirect(url_for('success'))

# Success page: Show a confirmation message after successful booking
@app.route('/success')
def success():
    return render_template('success.html')

# View all reservations: Display all bookings from the database
@app.route('/reservations')
def reservations():
    # Connect to the database and retrieve all bookings
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    bookings = c.fetchall()  # Fetch all rows from the table
    conn.close()

    # Pass the list of bookings to the template
    return render_template('reservations.html', bookings=bookings)

# Running the app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)
