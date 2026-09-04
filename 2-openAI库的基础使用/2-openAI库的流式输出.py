"""
案例：
    openAI库的流式输出

knowledge：
    1. 什么是流式输出
    系统在生成数据的过程中，不需要等全部内容完全生成完毕，而是生成一部分、立即向客户端推送并展示一部分。
    最常见的体验就是大语言模型（如 ChatGPT）打字机式的逐字/逐词显示效果。

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
        {"role": "system", "content": "你是一个python编程专家，并且话非常多"},
        {"role": "assistant", "content": "好的我是编程专家并且话非常多，你要问什么？"},
        {"role": "user", "content": "输出1-10的数字"}
    ],

    # 2.3 开启流式输出
    stream=True

)   # ctrl + alt + v  给client.chat.completions.create()生成一个response的返回值

# 3、处理结果

# 3.1 结果一般输出
# print(response.choices[0].message.content)

# 3.2 流式输出
for chunk in response:
    # 在使用 OpenAI SDK 处理流式输出时，应当先判断 choices 是否非空
    if chunk.choices: # 这里的写法涉及到了python中的列表的真值判断
        print(chunk.choices[0].delta.content,
              end=' ',        # 每一段之间以空格分隔
              flush =True       # 立刻刷新缓冲区
              )

# 这里对代码进行解释
"""
API 返回的 response 是一个包含大量元数据（模型名、Token 消耗、生成原因等）的嵌套对象，这行代码是在一层层“剥洋葱”：

response：调用 client.chat.completions.create(...) 拿到的完整返回对象。

.choices：一个候选回复列表（List）。由于 API 支持通过设置参数 n=2 让模型一次生成多份不同的回答，因此所有结果都装在 choices 列表里。

[0]：取出列表里的第一个候选回复。默认情况下 n=1，列表里只有一项，所以永远取下标 0。

.message：该候选回复对应的完整消息对象（包含 role、content 以及可能的 tool_calls 等字段）。

.content：最终的回复文本内容（也就是模型实际说出的那段话，类型为 str）。
"""