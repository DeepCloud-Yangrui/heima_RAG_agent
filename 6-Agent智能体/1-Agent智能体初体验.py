from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

@tool(description="查询天气")
def get_weather() -> str:
    return "晴天"

agent = create_agent(
    model=ChatTongyi(model='qwen-max'),     # 智能体的大脑LLM
    tools=[get_weather],                               # 工具，向智能体提供一个工具列表
    system_prompt="你是一个聊天助手，可以回答用户问题"   # 系统提示词
)

res = agent.invoke(  # 需要传入一个字典进去
    {
        "messages": [  # messages 注意s 它的value是一个列表
            {"role": "user", "content": "明天深圳的天气如何"},
        ]
    }
)

# print(res)
for msg in res["messages"]:
    # 方法1：直接用pretty_print()打印
    # msg.pretty_print()

    # 方法2：用tpye(msg).__name__
    print(type(msg).__name__,':',msg.content)