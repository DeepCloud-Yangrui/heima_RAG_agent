"""
案例
    langchain访问模型的流式输出
"""
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen")
result = model.stream(input="你好你是什么模型，介绍一下你自己,你能做什么")

for chunk in result:
    print(chunk,end='',flush=True)