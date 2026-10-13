"""
案例：
    使用langchain调用ollama本地聊天模型
"""
import os
# 1. 导入现代化 Chat 客户端和消息类
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

# 2. 初始化 Chat 客户端
chat = ChatOllama(
    # 使用云端大模型
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # model="qwen3.8-max-0902"

    # 使用ollama本地大模型
    # 如果使用ChatOllama的话，这里不需要写base_url
    model="qwen:latest"

)

# 3. 构造提问消息
# 这里的message是一个列表list
message = [
    ("system","你是一名田园诗人"),
    ("human","给我写一首唐诗"),
    ("ai","梅子金黄杏子肥，麦花雪白菜花稀。"),
    ("human","仿照上首，再写一首"),
    # SystemMessage(content="你是一名田园诗人"),
    # HumanMessage(content="给我写一首唐诗"),
    # AIMessage(content="梅子金黄杏子肥，麦花雪白菜花稀。日长篱落无人过，惟有蜻蜓蛱蝶飞。"),
    # HumanMessage(content="仿照上首，再写一首")
]

# 4. 列表包裹传入并流式输出
for chunk in chat.stream(message):
    print(chunk.content, end="", flush=True)

print()