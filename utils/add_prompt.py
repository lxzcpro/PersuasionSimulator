from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/Test")
db = client.chat_db
chat_settings_collection = db.chat_settings

# 定义多个 chat_id 和对应的系统提示词
data = [
    {"chat_id": "chat1", "system_prompt": "You've just recieved a poor grade on an important exam, and your parents found out. They are waiting for you to come home and expalin what happened."},
    {"chat_id": "chat2", "system_prompt": "You've been wanting a dog for a long time, and you finally decide to approach your parents about it. You find them in the kitchen, talking after dinner."},
    {"chat_id": "chat3", "system_prompt": "You and your group of friends are planning a vaction together, but there are differing opinions on the destination. Some want to go camping while others are leaning towards a beach for relaxation. You are leaning more towards the beach."},
    {"chat_id": "chat4", "system_prompt": "You're visiting a new wet market for the first time. The prices for some of the iteams you want to buy seem a bit higher then you expected. You decide to try and negotiate a discount with one of the vendors, even though you're not a regular customer."},
    {"chat_id": "chat5", "system_prompt": "You are a student who has been scheduled to participate in a school event, such as a debate competition or a cultural festival. However, you have a personal commitment or an urgent matter that requires your attention on the same day. You need to ask your school counselor for permission to be excused from the event."}
]

# 插入或更新每个 chat_id 的系统提示词
for item in data:
    chat_settings_collection.update_one(
        {"chat_id": item["chat_id"]},
        {"$set": {"system_prompt": item["system_prompt"]}},
        upsert=True
    )

print("Test data inserted/updated successfully.")
