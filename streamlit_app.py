import streamlit as st

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Dict
import operator
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langchain.callbacks.base import BaseCallbackHandler

from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel

#
# State of the graph. All information preserved as we walk through.
#
class AgentState(TypedDict):
    agent: str
    userState: Dict
    lnode: str

#
# Only used for streaming. We dont need this.
#
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

#
# Graph
#
class zoomHandler():
    def __init__(self):
        api_key=st.secrets["OPENAI_API_KEY"]
        self.model=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key)

        builder = StateGraph(AgentState)
        builder.add_node('front_end',self.frontEnd)
        builder.add_node('provide_live_schedule',self.provideLiveSchedule)
        builder.add_node('provide_day_schedule',self.provideDaySchedule)
        builder.add_node('provide_zoom_link',self.provideZoomLink)

        builder.set_entry_point('front_end')
        builder.add_conditional_edges('front_end',self.should_continue,
                                      {END:END, 
                                       "reflect":"reflect", 
                                       "provide_live_schedule":"provide_live_schedule", 
                                       "provide_day_schedule":"provide_day_schedule", 
                                       "provide_zoom_link":"provide_zoom_link"})
        builder.add_edge('provide_live_schedule',END)
        builder.add_edge('provide_day_schedule',END)
        builder.add_edge('provide_zoom_link',END)
        memory = SqliteSaver(conn=sqlite3.connect(":memory:", check_same_thread=False))
        self.graph = builder.compile(
            checkpointer=memory,
            # interrupt_after=['planner', 'generate', 'reflect', 'research_plan', 'research_critique']
        )
        print("Completed zoomHandler init")

        def frontEnd(self, state: AgentState):
            print(f"START: {__name__}")
            print(f"END: {__name__}")

        def provideLiveSchedule(self, state: AgentState):
            print(f"START: {__name__}")
            print(f"END: {__name__}")

        def provideDaySchedule(self, state: AgentState):
            print(f"START: {__name__}")
            print(f"END: {__name__}")

        def provideZoomLink(self, state: AgentState):
            print(f"START: {__name__}")
            print(f"END: {__name__}")

#
# Main code
#

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
        abot=zoomHandler()
        thread={"configurable":{"thread_id":"1"}}
        for s in abot.graph.run(thread):
            print(f"GRAPH RUN: {s}")
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            full_response = "This should be replaced by the real response from the Graph..."
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == '__main__':
    start_chat()
 