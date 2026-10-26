from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.tools import tool


@tool(description="获取股价，传入股票名称，返回字符串信息")
def get_price(name:str) -> str:
    return f"股票{name}的价格是20元"

@tool(description="获取股票信息，传入股票名称，返回字符串信息")
def get_info(name:str) -> str:
    return f"股票{name}是一家A股上市公司，专注于IT职业教育"


agent = create_agent(
    model=ChatTongyi(model='qwen-max'),  # 智能体的大脑LLM
    tools=[get_info,get_price],
    system_prompt="你是一个智能助手，可以回答股票相关问题，记住请告知我思考过程，让我知道你为什么调用某个工具"

)

for chunk in agent.stream(
{
        "messages": [{"role":"user","content":"船只教育股价多少，介绍一下"}],
    },
    stream_mode="values",
):
    latest_message=chunk['messages'][-1]
    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)


    if isinstance(latest_message,AIMessage) and latest_message.tool_calls:       # 如果有工具调用，就打印出所调用的工具名称
        tools_list=[tc['name'] for tc in latest_message.tool_calls]
        print(f"工具调用{tools_list}")