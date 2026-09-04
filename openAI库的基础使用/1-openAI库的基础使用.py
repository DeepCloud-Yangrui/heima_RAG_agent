"""
案例：
    openAI库的基本使用

knowledge：
    1. openAI库的基本使用的步骤
        获取client对象 -> 调用模型 -> 处理结果
"""
# 导包
from openai import OpenAI
from pyexpat.errors import messages

# 1、获取client客户端对象（实际上就是创建一个openAI类对象）
client = OpenAI(
    # 这里不用写APIKEY，已经把它封装到环境变量中了

    # 1-1 用阿里百炼云 云端模型
    # base_url="https://ws-67fv97lfzo7oavm4.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"

    base_url="http://localhost:11434/v1"

    # 1-2 用ollama本地模型
)

# 2、调用模型
response = client.chat.completions.create(
    # 2.1-1 选择云端模型
    # model="qwen3.8-max",

    # 2.1-2 选择ollama本地模型
    model="qwen",


    # 2.2 输入问题 messages是一个列表，在列表中需要填入的是 字典
    messages=[
        {"role": "system", "content": "你是一个python编程专家，并且不说废话，简单回答"},
        {"role": "assistant", "content": "好的我是编程专家并且话不多，你要问什么？"},
        {"role": "user", "content": "输出1-10的数字"}
    ]
)   # ctrl + alt + v  给client.chat.completions.create()生成一个response的返回值

# 3、处理结果
print(response.choices[0].message.content)

# 这里对代码进行解释
"""
API 返回的 response 是一个包含大量元数据（模型名、Token 消耗、生成原因等）的嵌套对象，这行代码是在一层层“剥洋葱”：

response：调用 client.chat.completions.create(...) 拿到的完整返回对象。

.choices：一个候选回复列表（List）。由于 API 支持通过设置参数 n=2 让模型一次生成多份不同的回答，因此所有结果都装在 choices 列表里。

[0]：取出列表里的第一个候选回复。默认情况下 n=1，列表里只有一项，所以永远取下标 0。

.message：该候选回复对应的完整消息对象（包含 role、content 以及可能的 tool_calls 等字段）。

.content：最终的回复文本内容（也就是模型实际说出的那段话，类型为 str）。
"""