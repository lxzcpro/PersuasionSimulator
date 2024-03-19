from http import HTTPStatus
import dashscope
import json

dashscope.api_key="your_api_key”
model_name = "qwen_max"

def call_with_messages(input):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': input}]
    
    model = getattr(dashscope.Generation.Models, model_name)
    response = dashscope.Generation.call(
        model,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
