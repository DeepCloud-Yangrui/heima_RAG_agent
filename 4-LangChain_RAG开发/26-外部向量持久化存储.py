from langchain_community.document_loaders import CSVLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

# Chroma 向量数据库（轻量级）
# 确保langchain-chroma、chromadb这两个库安装了，没有的话请pip install

# 只需要改变这一处， 把向量存储的实例从内存存储InMemoryVectorStore替换为chroma的就行了
## 替换前
# vector_store = InMemoryVectorStore(
#     embedding=DashScopeEmbeddings(),  # 选择文本转向量的模型
# )
##替换后
vector_store = Chroma(
    collection_name="test",  # 数据库名称,给当前的向量存储起个名
    embedding_function=DashScopeEmbeddings(),  # 选择文本转向量的模型
    persist_directory='./chroma_db',  # 指定向量存储的路径
)

# 创建加载器
loader = CSVLoader(
    file_path="./data/info.csv",
    encoding='utf-8',
    source_column='source',         # 指定本条数据的来源是哪里
    )

docs = loader.load()

# print(docs[2])

# 1. 向量存储的 新增、删除、检索操作

## 文档添加
vector_store.add_documents(
    # 核心参数1：
    documents=docs,  # 被添加的文档，类型要求是list[document]
    # 核心参数2；
    ids=['id'+str(i) for i in range(1,len(docs)+1)]            # 给添加的文档添加id（字符串） 类型是list[str],可以通过列表推导式

)
## 文档删除,传入列表[id,id,.....]
vector_store.delete(['id1','id2'])
## 文档检索  返回类型： list[document]
result = vector_store.similarity_search(
    query='python是不是简单易学呀',
    k=3,  # 返回的结果要几个，k=3，返回相似度最高的3个
    filter={'source': '黑马程序员'}  # 过滤条件，只返回source为python的数据
)
print(result)