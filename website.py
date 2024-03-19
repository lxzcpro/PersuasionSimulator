from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.qwen import call_with_messages

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # 使用 SQLite 数据库
db = SQLAlchemy(app)

class ChatRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    reply = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/reply', methods=['POST'])
def reply():
    message = request.form['message']
    reply = call_with_messages(message)  # Use your model to generate a reply
    record = ChatRecord(message=message, reply=reply)  # 创建新的聊天记录
    db.session.add(record)  # 添加到数据库会话
    db.session.commit()  # 提交会话
    return jsonify({'reply': reply})

@app.route('/')
def home():
    return render_template('chat.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建所有数据库表
    app.run(debug=True)