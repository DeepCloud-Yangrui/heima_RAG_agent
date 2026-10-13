from langchain_ollama import OllamaEmbeddings

# 切换阿里云模型到ollama本地模型只需要把模型类本身换了就行
model = OllamaEmbeddings(model="qwen3-embedding:4b")

# 不用invoke stream
# 使用的是embed_query和embed_documents这两个api，一个是单次转换，一个是批量转换
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你", "我稀饭你","我稀罕你"]))