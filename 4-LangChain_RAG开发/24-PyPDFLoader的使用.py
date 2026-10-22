from langchain_community.document_loaders import PyPDFLoader

# 实例化PyPDFLoader
loader = PyPDFLoader(
    file_path='./data/pdf2.pdf',
    mode='single',  # page模式，每个页面形成一个document文档对象
    # single模式，不管有多少页，只返回一个document文档对象
    # password='itheima'
)

i=0
for doc in loader.lazy_load():
    print(doc)
    i+=1
    print(i)