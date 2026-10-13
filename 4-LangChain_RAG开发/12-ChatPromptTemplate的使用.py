from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可以作诗"),
        # MessagesPlaceholder("history"), # 这里括号里的key任意起名，习惯上写history
        # test:不同的key
        MessagesPlaceholder('yangrui'),
        ("human", "请再来一首唐诗"),
    ]
)

# 准备一些历史消息
history_data=[
    # 这里的简化写法 ，详见笔记-09-langchain的消息简写形式
    ("human", "你来作一首唐诗"),
    ("ai", "床前明月光疑是地上霜举头望明月低头思故乡"),
    ("human", "好诗好诗再来一首"),
    ("ai", "锄禾日当午汗滴禾下土谁之盘中餐粒粒皆辛苦"),
]

# 注入历史消息,注意只能用invoke方法来注入
prompt_text = chat_prompt_template.invoke({"yangrui": history_data}).to_string()
print(prompt_text)

model = ChatTongyi(model="qwen-max")
res = model.invoke(prompt_text)


print(res.content)