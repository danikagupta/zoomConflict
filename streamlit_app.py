import streamlit as st
from graph import zoomHandler

DEBUGGING=0

def start_chat():
    st.title('Test Zoom Conflict Handler')
    avatars={"system":"💻🧠","user":"🧑‍💼","assistant":"🎓"}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar=avatars[message["role"]]
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatars["user"]):
            st.markdown(prompt)
        abot=zoomHandler(st.secrets['OPENAI_API_KEY'])
        thread={"configurable":{"thread_id":"1"}}
        for s in abot.graph.stream({'initialMsg':prompt},thread):
            if DEBUGGING:
                print(f"GRAPH RUN: {s}")
                st.write(s)
            for k,v in s.items():
                if DEBUGGING:
                    print(f"Key: {k}, Value: {v}")
                if resp := v.get("responseToUser"):
                    with st.chat_message("assistant", avatar=avatars["assistant"]):
                        st.write(resp)
                    st.session_state.messages.append({"role": "assistant", "content": s})

if __name__ == '__main__':
    start_chat()
 