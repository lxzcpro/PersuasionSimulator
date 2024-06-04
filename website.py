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

os.system("python utils/add_prompt.py")

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Test"
client = PyMongo(app)

users_collection = client.db.users
messages_collection = client.db.messages
feedback_collection = client.db.feedback

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
    username = session['username']
    message = request.json['message']
    chat_id = request.json.get('chat-id')
    timestamp = datetime.utcnow()
    
    messages_collection.insert_one({"username": username, "message": message, "timestamp": timestamp, "chat_id": chat_id})
    
    reply = call_with_messages(message, chat_id)
    
    messages_collection.insert_one({"username": "Bot", "user_chatting_with": username, "message": reply, "timestamp": timestamp, "chat_id": chat_id})
    time.sleep(1)
    
    messages = messages_collection.find({"chat_id": chat_id, "$or": [{"username": username}, {"user_chatting_with": username}]}).sort("timestamp", 1)
    messages = [message for message in messages]
    messages = to_json(messages)
    messages = json.loads(messages)
    
    return jsonify({'messages': messages, 'reply': reply})

@app.route('/load_chat', methods=['GET'])
def load_chat():
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']  # Get the username from the session
    chat_id = request.args.get('chat_id')  # Assuming chat_id is passed from the frontend
    # Get all messages for the logged-in user and specific chat
    messages = messages_collection.find({"chat_id": chat_id, "$or": [{"username": username}, {"user_chatting_with": username}]}).sort("timestamp", 1)
    # Convert the messages to a list of dictionaries
    messages = [message for message in messages]
    # Convert ObjectId to string
    for message in messages:
        message['_id'] = str(message['_id'])
    return jsonify({'messages': messages})

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']  # Get the username from the session
    message = request.json['message']  # Get the message from the request
    chat_id = request.json['chat_id']  # Get the chat_id from the request
    # Store the message in the database with the username and chat_id
    messages_collection.insert_one({"message": message, "username": username, "chat_id": chat_id, "timestamp": datetime.utcnow()})
    
    # 如果消息为空，直接返回，不插入数据库
    if message is None or message.strip() == '':
        return jsonify({"success": True})
    
    try:
        messages_collection.insert_one({
            "username": username,
            "message": message,
            "chat_id": chat_id,
            "timestamp": datetime.datetime.utcnow()
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/get_chat/<chat_id>/<user_id>', methods=['GET'])
def get_chat(chat_id, user_id):
    if 'username' not in session:
        return jsonify({"error": "Please log in to use the chat feature"})
    username = session['username']  # Get the username from the session
    # if username != user_id:
    #     return jsonify({"error": "Unauthorized access"})
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
        return render_template('login.html')

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
            session['username'] = username
            session['user_id'] = str(user['_id'])
            return jsonify({"message": "User logged in successfully", "success": True})
    else:
        return render_template('login.html')

    
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
        messages_collection.delete_many({"chat_id": chat_id, "$or": [{"username": username}, {"user_chatting_with": username}]})
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

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    timestamp = datetime.utcnow()
    
    feedback_collection.insert_one({
        "name": name,
        "email": email,
        "message": message,
        "timestamp": timestamp
    })
    
    return jsonify({"success": True, "message": "Your message has been sent successfully."})


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")