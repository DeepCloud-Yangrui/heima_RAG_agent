"""
案例：
    演示SystemMessage+HumanMessage
"""
import os
# 1. 导入现代化 Chat 客户端和消息类
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage

# 2. 初始化 Chat 客户端
chat = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen3.8-max-0902"
)

# 3. 构造提问消息
# 这里的message是一个列表list
message = [
    SystemMessage(content="你是一名田园诗人"),
    HumanMessage(content="给我写一首唐诗")
]

# 4. 列表包裹传入并流式输出
for chunk in chat.stream(message):
    print(chunk.content, end="", flush=True)

print()