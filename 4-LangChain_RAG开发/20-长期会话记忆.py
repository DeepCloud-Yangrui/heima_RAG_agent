import os,json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

"""
知识点：
    1、messages_from_dict函数可以将一个字典转换为一个messages对象，
    这个对象可以用于存储和管理会话信息。在会话中，我们可以存储用户输入、系统输出、用户反
    馈等信息，以便在后续的对话中继续使用这些信息。
    [字典，字典，字典] -> [消息、消息、消息]
    2、message_to_dict函数可以将一个messages对象（BaseMessage类实例）转换为一个字典
    3、AIMessage、HumanMessage、SystemMessage都是BaseMessage的子类
"""

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id        # 会话id
        self.storage_path = storage_path    # 不同会话id的存储文件所在的文件夹路径
        # 拼接出完整的文件路径
        self.file_path=os.path.join(self.storage_path, self.session_id)

        # 确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    def add_messages(self,messages:Sequence[BaseMessage] ) -> None:     # 这个方法继承自父类，需要对功能进行重写
        #:Sequence[BaseMessage] 是对messages参数类型注解
        # None是对返回值 的类型注解，表示不返回任何值
        # Sequence序列，类似list、tuple，看到Sequence当作list去用
        all_message = list(self.messages)       # 把已有的消息：self.messages转为list，用all_messages来记录
        all_message.extend(messages)          # 把新的消息：messages追加到all_message中,融合成一个list

        # 将数据同步写入本地文件中
        # 类对象写入文件 -> 得到一堆二进制，无法明文查看，不太方便
        # 为了方便，可以将BaseMessage转为字典，借助json模块以json字符串写入文件
        # 又通过官方提供的方法message_to_dict:可以完成将  单个消息对象（BaseMessage类示例） -> 字典

        # 写法1
        new_messages=[]
        for message in all_message:
            to_dict = message_to_dict(message)      # 消息转字典
            new_messages.append(to_dict)

        # 写法2，用列表的推导式来简化写法(写法1，2完全等价)
        new_messages=[message_to_dict(message) for message in all_message]

        # 将数据写入文件
        with open(self.file_path,'w',encoding='utf-8')as f:
            json.dump(new_messages,f)       # json.dump(file,f)方法，将file转为json再写入文件f中

    @property                   # @property装饰器，将方法转为属性，调用时不需要加括号
    def messages(self) -> list[BaseMessage]:
        # 当前文件内存放的： list[字典]
        try:
            # 如果一切正常：
            with open(self.file_path,'r',encoding='utf-8')as f:
                message_data = json.load(f)     # 返回值是： list[字典]
                # 但我们希望返回的是：-> list[BaseMessage]
                from_dict = messages_from_dict(message_data)
                return from_dict
        except FileNotFoundError:
            return []       #如果文件不存在，则返回空列表

    def clear(self) -> None:
        with open(self.file_path,'w',encoding='utf-8')as f:
            json.dump([],f)



## 直接导入19 的内容，部分修改

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
    print("=" * 20,'\n', full_prompt.to_string(), '\n',"=" * 20)
    return full_prompt


# 4.构建一个基础链base chain
base_chain = prompt | print_prompt | model | str_parser

# 5.创建一个新的链，对原有的基础链basechain有增强功能：自动附加历史消息
#
# # 创建一个字典来记录用户对话历史id，相当于一个数据库，用来存放不同用户的历史消息
# store = {}  # key就是session，value就是InMemoryChatMessageHistory类对象
#

# 实现get_history
def get_history(session_id):

    return FileChatMessageHistory(session_id,'./chat_history')

    # 如果刚开始运行，字典为空，需要判断
    # if session_id not in store:
    #     store[session_id] = InMemoryChatMessageHistory()
    # return store[session_id]


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

    # res = conversion_chain.invoke({"input": "小明有两个猫"}, session_config)
    # print("第1次执行：", res)
    #
    # res = conversion_chain.invoke({"input": "小明有一只狗"}, session_config)
    # print("第2次执行：", res)

    res = conversion_chain.invoke({"input": "小明总共有几个宠物"}, session_config)
    print("第3次执行：", res)