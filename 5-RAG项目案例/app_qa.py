import time
from rag import RagService
import config_data as config
import streamlit as st

st.title("智能客服")
st.divider()              # 分隔符
# rag_service = RagService()    用户输入内容后页面一刷新，就会重新创建ragservice的对象，所以也存到st.session_state中

if 'rag' not in st.session_state:
    st.session_state["rag"] = RagService()


if 'message' not in st.session_state:
    st.session_state["message"] = [
        {
            "role": "assistant",
            "content": "你好！有什么可以帮助你的吗？"
        }
    ]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
# 在页面最下方提供用户输入框
prompt = st.chat_input()

if prompt:              # 这是在？
    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append(
        {"role":"user","content":prompt}
    )

    ai_res_list=[]
    with st.spinner("AI思考中......"):
        time.sleep(1)

        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        # st.chat_message("assistant").write(res)
        # streamlit中也有流式输出的方法
        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))

        # st.chat_message("assistant").write("你好！")
        st.session_state["message"].append(

            {"role":"assistant","content":"".join(ai_res_list)}
        )