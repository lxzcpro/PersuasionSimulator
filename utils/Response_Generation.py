from http import HTTPStatus
import dashscope
import json

def Response_Generation(input, model_name):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': "我希望你能成为语言的艺术大师，帮助我在困境中给出给力的回复。我会给你一句话或一段话，你需要给出一句或多句的回复。你的回复需要能够从心底上打动对方，语言得体，逻辑清晰，用词合理。你的回答应该仅包含回复以及根据对方语气所判断的回复的成功概率，两者之间需要换行。"},
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
