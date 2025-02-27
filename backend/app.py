from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import random
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=devops-student-portal-app-db-server.database.windows.net,1433;'
        'DATABASE=devops-student-portal-app-sql;'
        'UID=uva_student;'
        'PWD=Whisperer123'
    )
    return conn

# Sample chatbot responses
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help?"],
    "how are you": ["I'm just a bot, but I'm doing fine!", "I'm great! What about you?"],
    "bye": ["Goodbye!", "See you later!", "Bye! Have a great day!"],
}

def chatbot_response(message):
    """Generate a chatbot response based on input message"""
    message = message.lower().strip()
    for key in responses:
        if key in message:
            return random.choice(responses[key])
    return "I'm not sure how to respond to that."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat-password')

        # Validate server-side
        if not name or not email or not password:
            return jsonify({"success": False, "error": "Missing required fields."}), 400

        if len(password) < 8:
            return jsonify({"success": False, "error": "Password must be at least 8 chars."}), 400

        if repeat_password and password != repeat_password:
            return jsonify({"success": False, "error": "Passwords do not match."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if student already exists
        cursor.execute("SELECT id FROM Student WHERE email = ?", email)
        existing_student = cursor.fetchone()
        if existing_student:
            flash('Email already registered', 'danger')
            conn.close()
            return redirect(url_for('register'))

        # Hash password and insert new student
        hashed_password = generate_password_hash(password, method='sha256')
        cursor.execute("""
            INSERT INTO Student (name, email, password)
            VALUES (?, ?, ?)
        """, name, email, hashed_password)

        conn.commit()
        conn.close()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        # Select the columns you need. In this example:
        # id, name, email, password, program_id
        cursor.execute("""
            SELECT id, name, email, password, program_id
            FROM Student
            WHERE email = ?
        """, email)
        student = cursor.fetchone()
        conn.close()

        if student and check_password_hash(student[3], password):
            session['user_id'] = student[0]  # student[0] is the `id`
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/profile")
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, program_id
        FROM Student
        WHERE id = ?
    """, user_id)
    student = cursor.fetchone()
    conn.close()

    # `student` is a tuple (id, name, email, program_id).
    # You can pass it to the template to show the user’s info.
    return render_template("profile.html", student=student)

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from frontend"""
    user_message = request.json.get("message", "")
    bot_reply = chatbot_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
