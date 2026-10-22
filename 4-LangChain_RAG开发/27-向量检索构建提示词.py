"""
提示词：用户的提问 + 向量库中检索到的参考资料
"""
import time

from dashscope.cli.fine_tunes import stream
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatTongyi(model="qwen-max")

prompt = ChatPromptTemplate.from_messages(
    [('system', '以我提供的已知参考资料为主，简介和专业地回答用户问题。参考资料：{context}'),
     ('user', '用户提问：{question}')],
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model='text-embedding-v4'), )

# 准备参考资料（向量库的数据）

# add_texts 传入一个list[str] 因为是测试学习，用这个方法就行
vector_store.add_texts(
    ['减肥就是要少吃多练', '在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来', '跑步是很好的运动哦'])

# 用户提问：
input_text = '怎么减肥'

# 检索向量库
result = vector_store.similarity_search(input_text, 2)

# print(result)
# print('='*50)
reference_text = '['
for doc in result:
    reference_text += doc.page_content
reference_text += ']'
print(reference_text)


# 为了便于调试，写一个函数加入到链中,在提示词交给model之前，这个函数能够把提示词的内容输出出来方便调试等
def print_prompt(full_prompt):
    print(full_prompt)
    print('=' * 50)
    return full_prompt


# 构建链
chain = prompt |print_prompt| model | StrOutputParser()

res = chain.stream({"context": reference_text, "question": input_text, })

for chunk in res:
    print(chunk,end='',flush=True)
