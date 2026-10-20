from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

# 创建所需的解析器
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

# 创建模型
model = ChatTongyi(model='qwen-max',streaming=True)

# 创建第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "我邻居姓{lastname},他生了一个{gender}，请帮忙起名字，仅告诉我名字，并封装为json格式返回给我，"
    "要求key是name，value就是你起的名字，请严格遵守格式要求"  # 这里在提示词中要求了返回结果的格式
)

# 创建第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名:{name},请帮我解析姓名的含义"
)

# 构建链
chain = first_prompt | model | json_parser |second_prompt|model|str_parser
# res = chain.invoke({"lastname": "张", "gender": "女儿"})

# 如果要改为流式输出，改用stream方法
chunks=chain.stream({"lastname": "张", "gender": "女儿"})

# 循环语句打印流式输出
for chunk in chunks:
    print(chunk, end='',flush=True)





# print(type(res))
