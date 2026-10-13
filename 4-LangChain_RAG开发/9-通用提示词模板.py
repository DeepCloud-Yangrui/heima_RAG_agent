from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
# zero-shot

# 1、实例化PromptTemplate来调用from_template方法
prompt_template = PromptTemplate.from_template("我的邻居姓{lastname},刚生了{gender}，你帮我起个名字，简单回答")

# 2、调用fromat()方法，实现文本注入
prompt_text = prompt_template.format(lastname="张", gender="女儿")

# print(prompt_text)
model = Tongyi(model="qwen-max")

chain=prompt_template|model
chain.invoke(input={"lastname":"张", "gender":"女儿"})     # 这里需要写一个字典

res = model.invoke(input=prompt_text)
print(res)
