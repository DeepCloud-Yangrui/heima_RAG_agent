from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

parser = StrOutputParser()  # 这里创建parser对象，不用传入参数
model = ChatTongyi(model="qwen-max")
prompt = PromptTemplate.from_template(
    "我邻居姓{lastname}，刚生了个{gender}，请起名字，仅仅告知我名字，无需其他内容"
)
chain = prompt | model | parser | model |parser # 直接把parse加入两个model之间

res: AIMessage = chain.invoke({"lastname": "张", "gender": "女儿"})
print(res)
print(type(res))
