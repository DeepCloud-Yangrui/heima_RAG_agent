from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",       # 指定编码为utf-8
    csv_args={
        "delimiter":"," ,    # 指定分隔符
        'quotechar':'"' ,     # 指定包裹带有分割符的整体用什么包裹
        # 如果数据原本有表头，就不要使用fieldnames参数，否则会把原有的表头也当作是一行数据加载出来
        "fieldnames":['a','b','c','d']

    }
)

# 批量加载

"""documents = loader.load()
for document in documents:
    print(type(document),document)"""

# 懒加载   .lazy_load()方法

documents = loader.lazy_load()
# print(type(documents))
for document in documents:
    print(document)
