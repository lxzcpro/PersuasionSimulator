from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from utils.qwen import call_with_messages
from datetime import datetime
from bson import json_util
import dashscope
import os
import time
import json

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Test"
client = PyMongo(app)

users_collection = client.db.users
messages_collection = client.db.messages

def to_json(data):
    return json_util.dumps(data)

@app.route('/save_api_key', methods=['POST'])
def save_api_key():
    api_key = request.form.get('api-key')
    if not api_key:
        return jsonify({"error": "API key not provided"})
    dashscope.api_key = api_key
    return jsonify({"success": True})

@app.route('/reply', methods=['POST'])
def reply():
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']  # Get the username from the session
    message = request.json['message']
    chat_id = request.json.get('chat-id')  # Assuming chat_id is passed from the frontend
    timestamp = datetime.utcnow()  # Use UTC time for consistency across different time zones
    # Save the user's message to the database
    messages_collection.insert_one({"username": username, "message": message, "timestamp": timestamp, "chat_id": chat_id})
    # Generate a reply
    reply = call_with_messages(message)  # Use your model to generate a reply
    # Save the reply to the database
    messages_collection.insert_one({"username": "Bot", "message": reply, "timestamp": timestamp, "chat_id": chat_id})
    time.sleep(1)  # Wait for the new messages to be written to the database
    # Get all messages for the current user and chat
    messages = messages_collection.find({"chat_id": chat_id}).sort("timestamp", 1)
    # Convert the messages to a list of dictionaries
    messages = [message for message in messages]
    messages = to_json(messages)
    messages = json.loads(messages)  # Convert the JSON string back to a Python object
    return jsonify({'messages': messages, 'reply': reply})

@app.route('/load_chat', methods=['GET'])
def load_chat():
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']  # Get the username from the session
    chat_id = request.args.get('chat_id')  # Assuming chat_id is passed from the frontend
    # Get all messages for the logged-in user and specific chat
    messages = messages_collection.find({"chat_id": chat_id}).sort("timestamp", 1)
    # Convert the messages to a list of dictionaries
    messages = [message for message in messages]
    return jsonify({'messages': messages})

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return "Error: Please log in to use the chat feature"
    username = session['username']  # Get the username from the session
    chat_id = request.json.get('chat-id')
    message = request.json.get('message')
    timestamp = datetime.utcnow()  # Use UTC time for consistency across different time zones
    messages_collection.insert_one({"chat_id": chat_id, "username": username, "message": message, "timestamp": timestamp})
    return "Message sent successfully"

@app.route('/get_chat/<chat_id>/<user_id>', methods=['GET'])
def get_chat(chat_id, user_id):
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']  # Get the username from the session
    if username != user_id:
        return jsonify({"error": "Unauthorized access"})
    # Get messages for the specified chat_id and username
    messages = messages_collection.find({"chat_id": chat_id, "username": username}).sort("timestamp", 1)
    # Convert the messages to a list of dictionaries
    messages = [message for message in messages]
    
    # Convert ObjectId to string
    for message in messages:
        message['_id'] = str(message['_id'])
    
    return jsonify({'messages': messages})

# @app.route('/get_chat', methods=['GET'])
# def get_chat_redirect():
#     if 'username' not in session:
#         return jsonify({"error": "Please log in to use the chat feature"})
#     chat_id = request.args.get('chat_id')  # Assuming chat_id is passed from the frontend
#     return redirect(url_for('get_chat', chat_id=chat_id))


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
            return jsonify({"message": "Error: User already exists", "success": False})
        else:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({"username": username, "password": hashed_password})
            return jsonify({"message": "User registered successfully", "success": True})
    else:
        return render_template('login.html')  # Assuming you have a register.html file in your templates folder

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_collection.find_one({"username": username})
        if not user:
            return jsonify({"message": "Error: User does not exist", "success": False})
        elif not check_password_hash(user["password"], password):
            return jsonify({"message": "Error: Incorrect password", "success": False})
        else:
            session['username'] = username  # Store the username in the session
            return jsonify({"message": "User logged in successfully", "success": True})
    else:
        return render_template('login.html')  # Assuming you have a login.html file in your templates folder
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"message": "User logged out successfully", "success": True})

@app.route('/clear_chat/<chat_id>/<user_id>', methods=['POST'])
def clear_chat(chat_id, user_id):
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']
    try:
        # 删除特定用户在特定聊天下的所有消息，包括与机器人的聊天记录
        messages_collection.delete_many({"chat_id": chat_id, "username": {"$in": [username, user_id]}})
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
