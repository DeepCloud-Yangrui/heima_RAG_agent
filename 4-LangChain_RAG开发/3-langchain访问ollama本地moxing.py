"""
案例
    langchain访问ollama本地模型
"""
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen")
result = model.invoke(input="你好你是什么模型，介绍一下你自己,你能做什么")
print(result)