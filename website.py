from flask import Flask, request, jsonify, render_template, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from utils.qwen import call_with_messages

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Persuasion"
client = PyMongo(app)

@app.route('/reply', methods=['POST'])
def reply():
    message = request.form['message']
    reply = call_with_messages(message)  # Use your model to generate a reply
    return jsonify({'reply': reply})

# Connect to MongoDB
users_collection = client.db.users

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
            return "User logged in successfully"
    else:
        return render_template('login.html')  # Assuming you have a login.html file in your templates folder
    
@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
