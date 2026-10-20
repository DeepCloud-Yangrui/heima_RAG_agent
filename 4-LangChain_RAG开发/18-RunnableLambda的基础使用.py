from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

# 创建模型
model = ChatTongyi(model="qwen-max",streaming=True)         # 开启流式输出

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

# 创建提示词模板
first_prompt = PromptTemplate.from_template(
    "我邻居姓{lastname},生了一个{gender}，请你帮忙起一个名字，仅告知我名字，不要额外信息"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name},请解析它的含义"
)

# 创建chain

# 上节AIMessage转换为dict是json_parser完成的，本节用lambda来完成
# 函数lambda的入参：AIMessage类对象 --> 返回值：dict{"name":"xxx"}
# my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

chain = first_prompt | model | (lambda ai_msg:{"name":ai_msg.content})| second_prompt | model | str_parser

# invoke 注入方法
# res = chain.invoke({"lastname": "张", "gender": "女儿"})
# print(res)

# stream流式输出方法
chunks = chain.stream({"lastname": "张", "gender": "女儿"})
for chunk in chunks:
    print(chunk,end='',flush=True)