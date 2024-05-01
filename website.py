from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from utils.qwen import call_with_messages
from datetime import datetime
from utils.tools import jsonify

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Persuasion"
client = PyMongo(app)

users_collection = client.db.users
messages_collection = client.db.messages

@app.route('/reply', methods=['POST'])
def reply():
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']  # Get the username from the session
    message = request.form['message']
    timestamp = datetime.utcnow()  # Use UTC time for consistency across different time zones
    # Save the user's message to the database
    messages_collection.insert_one({"username": username, "message": message, "timestamp": timestamp})
    # Generate a reply
    reply = call_with_messages(message)  # Use your model to generate a reply
    # Save the reply to the database
    messages_collection.insert_one({"username": "Bot", "message": reply, "timestamp": timestamp})
    # Get all messages
    messages = messages_collection.find().sort("timestamp", 1)  # Sort by timestamp in ascending order
    # Convert the messages to a list of dictionaries
    messages = [message for message in messages]
    return jsonify({'messages': messages, 'reply': reply})

@app.route('/load_chat', methods=['GET'])
def load_chat():
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    # Get all messages
    messages = messages_collection.find().sort("timestamp", 1)  # Sort by timestamp in ascending order
    # Convert the messages to a list of dictionaries
    messages = [message for message in messages]
    return jsonify({'messages': messages})

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return "Error: Please log in to use the chat feature"
    username = session['username']  # Get the username from the session
    message = request.form.get('message')
    timestamp = datetime.utcnow()  # Use UTC time for consistency across different time zones
    messages_collection.insert_one({"username": username, "message": message, "timestamp": timestamp})
    return "Message sent successfully"

@app.route('/get_messages', methods=['GET'])
def get_messages():
    if 'username' not in session:
        return "Error: Please log in to use the chat feature"
    username = session['username']  # Get the username from the session
    messages = messages_collection.find({"username": username})
    return jsonify([message for message in messages])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_collection.find_one({"username": username})
        if user:
            return "Error: User already exists"
        else:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({"username": username, "password": hashed_password})
            return "User registered successfully"
    else:
        return render_template('login.html')  # Assuming you have a register.html file in your templates folder

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_collection.find_one({"username": username})
        if not user:
            return "Error: User does not exist"
        elif not check_password_hash(user["password"], password):
            return "Error: Incorrect password"
        else:
            session['username'] = username  # Store the username in the session
            messages = messages_collection.find({"username": username})
            return jsonify([message for message in messages])
    else:
        return render_template('login.html')  # Assuming you have a login.html file in your templates folder
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
    
@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
