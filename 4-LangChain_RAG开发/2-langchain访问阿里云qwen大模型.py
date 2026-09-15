import os

from langchain_community.llms.tongyi import Tongyi


model = Tongyi(model="qwen-max",
               )
result = model.invoke(input="哈啰你好，你是谁，你能做什么")
print(result)
