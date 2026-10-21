from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 实例化文本加载器
loader = TextLoader(file_path='./data/Python基础语法.txt', encoding='utf-8', )

docs = loader.load()

# 实例化文本分割器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 分段的最大字符数
    chunk_overlap=50,  # 分段之间运行重叠的字符数
    # 文本自然段落分割的依据符号,按照先后顺序是存在优先级的
    separators=['\n\n', '\n', '。', '！', '？', '，', ',', '.', '?', '!', ' ', ''],
    length_function=len  # 统计每个chunk中有多少字符的依据函数

)

split_docs = splitter.split_documents(docs)
print(len(split_docs))      # 统计docs被分割成了多少个chunks

for chunk in split_docs:
    print('='*50,'\n',chunk,'='*50,'\n')
# print(docs)
# print(len(docs))