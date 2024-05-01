import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig

model_path = "/root/workspaces/ckpts/Baichuan2-7B-Chat"

tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained(model_path)

messages = []
messages.append({"role": "user", "content": "请问西湖大学创新班的报考条件是什么"})
response = model.chat(tokenizer, messages)
print(response)