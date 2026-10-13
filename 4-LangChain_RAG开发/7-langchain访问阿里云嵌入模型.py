from langchain_community.embeddings import DashScopeEmbeddings  # 导入阿里云的嵌入模型类DashScopeEmbeddings

# 创建模型对象 类（）里不传model的话默认用的是text-embedding-v1
model = DashScopeEmbeddings()

# 不用invoke stream
# 使用的是embed_query和embed_documents这两个api，一个是单次转换，一个是批量转换
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你", "我稀饭你","我稀罕你"]))