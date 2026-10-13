from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate,ChatPromptTemplate

template = PromptTemplate.from_template("我的邻居是{lastname},最喜欢{hobby}")
res = template.format(lastname="张", hobby="钓鱼")
print(res,type(res))
res2 = template.invoke({"lastname": "周杰伦", "hobby": "唱歌"})
print(res2,type(res2))
