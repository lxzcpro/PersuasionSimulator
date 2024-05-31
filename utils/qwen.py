from pymongo import MongoClient
from http import HTTPStatus
import dashscope

# dashscope.api_key="your_api_key”

model_name = "qwen_turbo"
client = MongoClient("mongodb://localhost:27017/Test")
db = client.chat_db
chat_settings_collection = db.chat_settings

def get_system_prompt(chat_id):
    setting = chat_settings_collection.find_one({"chat_id": chat_id})
    if setting and "system_prompt" in setting:
        return setting["system_prompt"]
    return "You are a helpful assistant."

def call_with_messages(input, chat_id):
    system_prompt = get_system_prompt(chat_id)
    messages = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': input}]
    
    model = getattr(dashscope.Generation.Models, model_name)
    response = dashscope.Generation.call(
        model,
        messages=messages,
        result_format='message',
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))