from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/Test")
db = client.chat_db
chat_settings_collection = db.chat_settings

# 定义多个 chat_id 和对应的系统提示词
data = [
    {"chat_id": "chat1", "system_prompt": "You are Kobe Bryant."},
    {"chat_id": "chat2", "system_prompt": "You are Steven Hawking."},
    {"chat_id": "chat3", "system_prompt": "You are Joe Biden."}
]

# 插入或更新每个 chat_id 的系统提示词
for item in data:
    chat_settings_collection.update_one(
        {"chat_id": item["chat_id"]},
        {"$set": {"system_prompt": item["system_prompt"]}},
        upsert=True
    )

print("Test data inserted/updated successfully.")
