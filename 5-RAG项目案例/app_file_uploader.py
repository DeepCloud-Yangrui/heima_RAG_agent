"""
基于Streamlit完成WEB网页上传服务

    Streamlit的一个特殊/核心的机制：当web界面元素发生变化，则代码重新执行一遍

"""
import time
from itertools import count

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# file uploader，st.file_uploader 会在页面上生成一个“拖拽或点击上传”的区域
uploader_file = st.file_uploader(
    "请上传TXT文件",         ## 控件上方的提示文字
    type=['txt'],               # 只允许上传 .txt 文件
    accept_multiple_files=False  # 是否接受多文件上传
)

# session_state就是一个字典，它不会随着页面的刷新而刷新
if 'service' not in st.session_state:
    st.session_state['service']=KnowledgeBaseService()

if 'counter' not in st.session_state:
    st.session_state['counter']=0



if uploader_file is not None:
    # Streamlit 每次页面交互都会重跑整个脚本。首次打开时没人上传，uploader_file 为 None，
    # if 不成立，下面的代码不执行；用户上传后脚本重跑，这次 uploader_file 有值，才进入分支

    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type}|大小：{file_size:.2f}KB")

    # 获取上传文件的内容:  text -> byte字节数组类型 -> decode(utf-8) -> 字符串类型
    text = uploader_file.getvalue().decode('utf-8')
    # st.subheader(f"文件内容")

    with st.spinner('载入知识库中.....'):          # 在spinner内的代码执行过程中，会有一个转圈动画
        time.sleep(1)
        st.write(text)
        result = st.session_state['service'].upload_by_str(text, file_name)

    st.write(result)

