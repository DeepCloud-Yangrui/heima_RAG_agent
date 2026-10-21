from langchain_community.document_loaders import JSONLoader

# 创建类的实例

# 1. 从json对象中抽取内容
# loader = JSONLoader(
#     file_path='./data/stu.json',
#     jq_schema='.',
#     text_content=False,         # 告知jsonloader抽取的内容不是字符串
# )
# documents = loader.load()
#
# print(documents)

# 2. 从json数组中抽取对象
# loader = JSONLoader(
#     file_path='./data/stus.json',
#     jq_schema='.[].name',
#     text_content=False,         # 告知jsonloader抽取的内容不是字符串
# )
# documents = loader.load()
#
# print(documents)

# 3. 从json lines文件中读取对象
loader = JSONLoader(
    file_path='./data/stu_json_lines.json',
    jq_schema='.name',
    text_content=False,         # 告知jsonloader抽取的内容不是字符串
    json_lines=True,            # 告知jsonloader这是一个jsonlines文件
)
documents = loader.load()

print(documents)