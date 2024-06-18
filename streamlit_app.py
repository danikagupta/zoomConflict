import streamlit as st

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Dict
import operator
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langchain.callbacks.base import BaseCallbackHandler

from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel

import sqlite3

from zoom_api import *

#
# State of the graph. All information preserved as we walk through.
#
class AgentState(TypedDict):
    agent: str
    userState: Dict
    lnode: str
    initialMsg: str
    responseToUser: str

class Category(BaseModel):
    category: str
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
        builder.add_node('provide_zoom_code',self.provideZoomCode)
        builder.add_node('provide_zoom_link',self.provideZoomLink)

        builder.set_entry_point('front_end')
        builder.add_conditional_edges('front_end',self.main_router,
                                      {END:END, 
                                       "provide_live_schedule":"provide_live_schedule", 
                                       "provide_zoom_code":"provide_zoom_code", 
                                       "provide_zoom_link":"provide_zoom_link"})
        builder.add_edge('provide_live_schedule',END)
        builder.add_edge('provide_zoom_code',END)
        builder.add_edge('provide_zoom_link',END)
        memory = SqliteSaver(conn=sqlite3.connect(":memory:", check_same_thread=False))
        self.graph = builder.compile(
            checkpointer=memory,
            # interrupt_after=['planner', 'generate', 'reflect', 'research_plan', 'research_critique']
        )
        print("Completed zoomHandler init")

    def frontEnd(self, state: AgentState):
        print(f"START: frontEnd")
        my_prompt=f"""
                Please classify the user's request.
                If the user is unable to join a Zoom session due to a conflict, category is 'Conflict'
                If the user wants you to cancel an existing Zoom session, category is 'Cancel'
                If the user wants you to create a new Zoom session, category is 'Create'
                Else the category is 'Other'
                """
        category=self.model.with_structured_output(Category).invoke([
            SystemMessage(content=my_prompt),
            HumanMessage(content=state['initialMsg']),
        ]).category
        print(f"Category: {category}")
        print(f"END: frontEnd")
        return {
            'lnode':'front_end',
            'category':category        
        }

    def provideLiveSchedule(self, state: AgentState):
        print(f"START: provideLiveSchedule")
        responseToUser= get_scheduled_zoom_api_response()
        responseToUser= get_current_zoom_api_response()
        print(f"END: provideLiveSchedule")
        return {
            'lnode':'provide_live_schedule',
            'responseToUser':responseToUser
        }

    def provideZoomCode(self, state: AgentState):
        print(f"START: provideZoomCode")
        responseToUser= get_host_code(1)
        print(f"END: provideZoomCode")
        return {
            'lnode':'provide_day_schedule',
            'responseToUser':responseToUser
        }

    def provideZoomLink(self, state: AgentState):
        print(f"START: provideZoomLink")
        responseToUser= "Sorry. I do not have the ability to create Zoom links yet. Please wait for a human to respond."
        print(f"END: provideZoomLink")
        return {
            'lnode':'provide_zoom_link',
            'responseToUser':responseToUser
        }

    def main_router(self, state: AgentState):
        print(f"START: mainRouter with msg {state['initialMsg']} and category {state['category']}")
        if state['category'] == 'Conflict':
            return "provide_live_schedule"
        elif state['category'] == 'Cancel':
            return "provide_zoom_code"
        elif state['category'] == 'Create':
            return "provide_zoom_link"
        elif state['category'] == 'Other':
            print(f"Content not relevant to Zoom. Ignoring. {state['initialMsg']}")
            return END
        else:
            print(f"Unknown category {state['category']}")
            return END

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
        for s in abot.graph.stream({'initialMsg':prompt},thread):
            print(f"GRAPH RUN: {s}")
            #st.write(s)
            for k,v in s.items():
                print(f"Key: {k}, Value: {v}")
                if resp := v.get("responseToUser"):
                    with st.chat_message("assistant", avatar=avatars["assistant"]):
                        st.write(resp)
                #st.write(s)
                #full_response = "This should be replaced by the real response from the Graph..."
                #st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": s})

if __name__ == '__main__':
    start_chat()
 