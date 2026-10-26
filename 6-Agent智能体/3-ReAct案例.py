from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

@tool(description="获取体重，返回值是整数，单位kg")
def get_weight() -> int:
    return 90


@tool(description="获取身高，返回值是整数，单位厘米")
def get_height() -> int:
    return 172




agent = create_agent(
    model=ChatTongyi(model='qwen-max'),  # 智能体的大脑LLM
    tools=[get_height,get_weight],
    system_prompt="你是严格遵循ReAct框架的智能体，必须按照[思考 -> 行动 ——> 观察 -> 再思考]的流程解决问题"
                  "且每轮仅能思考并调用1个工具，禁止单次调用多个工具。"
                  "并告知我你的思考过程，工具的调用原因，按思考，行动，观察三个结构告诉我"

)

for chunk in agent.stream(
{
        "messages": [{"role":"user","content":"计算我的BMI"}],
    },
    stream_mode="values",
):
    latest_message=chunk['messages'][-1]
    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)


    if isinstance(latest_message,AIMessage) and latest_message.tool_calls:       # 如果有工具调用，就打印出所调用的工具名称
        tools_list=[tc['name'] for tc in latest_message.tool_calls]
        print(f"工具调用{tools_list}")