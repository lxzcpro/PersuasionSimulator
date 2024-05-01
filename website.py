from flask import Flask, request, jsonify, render_template
from utils.qwen import call_with_messages

app = Flask(__name__)

@app.route('/reply', methods=['POST'])
def reply():
    message = request.form['message']
    reply = call_with_messages(message)  # Use your model to generate a reply
    return jsonify({'reply': reply})

@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)