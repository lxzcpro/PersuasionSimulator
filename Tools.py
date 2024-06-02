from http import HTTPStatus
import dashscope
import json
import gradio as gr
from utils.Sentiment_Analysis import Sentiment_Analyse
from utils.Response_Generation import Response_Generation

def response(input, model_name, task):
    if task == "Response_Generation":
        response = Response_Generation(input, model_name)
        return response.output.choices[0].message.content
    if task == "Sentiment_Analyse":
        if model_name == "qwen_turbo":
            response = Sentiment_Analyse(input, "qwen_turbo")
            return response.output.choices[0].message.content
        if model_name == "chatglm3-6b":
            response = Sentiment_Analyse(input, "chatglm3-6b")
            return response.output.choices[0].message.content

if __name__  == "__main__":

    demo = gr.Interface(
        response,
        [
            gr.Textbox(label="Input"),
            gr.Radio(["qwen_turbo", "chatglm3-6b"], label="Model"), #FIXME: model switch
            gr.Radio(["Response_Generation", "Sentiment_Analyse"], label="Task"),
        ],
        "text",
        title="A Useful Tool for Sentiment Analysis and Response Generation",
    )

    demo.launch()