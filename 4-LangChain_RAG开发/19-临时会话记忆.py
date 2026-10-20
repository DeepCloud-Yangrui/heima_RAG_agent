from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 1.创建模型
model = ChatTongyi(model="qwen-max", streaming=True)

# 2.创建提示词模板
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回答用户问题，对话历史{chat_history}，用户提问{input}，请回答"
# )

# 2-new 用聊天提示词模板ChatPromptTemplate来优化代替通用提示词模板PromptTemplate，
# 用聊天提示词模板（为什么要用ChatPromptTemplate来优化？）
prompt = ChatPromptTemplate.from_messages(
    [("system", "你需要根据会话历史回答用户问题，对话历史:"),
     MessagesPlaceholder('chat_history'),
     ("human", "请回答如下问题:{input}"), ])

# 3.创建字符串输出解析器
str_parser = StrOutputParser()


#
def print_prompt(full_prompt):
    print("=" * 20, full_prompt.to_string(), "=" * 20)
    return full_prompt


# 4.构建一个基础链base chain
base_chain = prompt | print_prompt | model | str_parser

# 5.创建一个新的链，对原有的基础链basechain有增强功能：自动附加历史消息

# 创建一个字典来记录用户对话历史id，相当于一个数据库，用来存放不同用户的历史消息
store = {}  # key就是session，value就是InMemoryChatMessageHistory类对象


# 实现get_history
def get_history(session_id):
    # 如果刚开始运行，字典为空，需要判断
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# 需要往里面传四个主要的参数
conversion_chain = RunnableWithMessageHistory(
    base_chain,  # 被增强的原有链
    get_history,  # 获取历史消息的函数，通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",  # 表示 用户输入 在模板中的占位符
    history_messages_key="chat_history"  # 历史消息在模板中的占位符
)

# 建立好加强链之后，来实现业务
if __name__ == '__main__':
    # 固定格式，添加LangChain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    res = conversion_chain.invoke({"input": "小明有两个猫"}, session_config)
    print("第1次执行：", res)

    res = conversion_chain.invoke({"input": "小明有一只狗"}, session_config)
    print("第2次执行：", res)

    res = conversion_chain.invoke({"input": "小明总共有几个宠物"}, session_config)
    print("第3次执行：", res)
