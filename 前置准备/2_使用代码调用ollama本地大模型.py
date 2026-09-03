"""
案例：
    使用代码来调用ollama本地大模型
回顾：
    只要修改两个地方
    1、APIKEY修改为：
    2、base_url修改为：


"""

from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # api_key="sk-ws-H.PMMIPYL.jJ7H.MEQCIDLmiNz4lm89VfUG8puAl4H7zPkESKTEURQerH_M3d8yAiAYzDDUbiHEyN7Xg5gIboloEWjwbvbB0RrZbQRKg682ow",
    base_url="http://localhost:11434/v1",
)

messages = [{"role": "user", "content": "你是哪个模型"}]
completion = client.chat.completions.create(
    model="qwen",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)