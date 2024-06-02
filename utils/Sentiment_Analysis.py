from http import HTTPStatus
import dashscope
import json

def Sentiment_Analyse(input, model_name):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': "假设你是一个具有情感分析能力的AI助手，你的用户收到了一个消息，但他们不确定消息中的情感表达。你的任务是帮助用户理解消息中的情感。请对接下来的文本进行情感分析，并请严格按照以下格式回答：'情感：{情感类型}，信心水平：{百分比}'。待分析的文本是："},
                {'role': 'user', 'content': input}]
    
    model = getattr(dashscope.Generation.Models, model_name)
    response = dashscope.Generation.call(
        model,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        return response
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

