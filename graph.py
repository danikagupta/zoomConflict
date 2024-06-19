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

import os


#
# State of the graph. All information preserved as we walk through.
#
class AgentState(TypedDict):
    agent: str
    userState: Dict
    lnode: str
    initialMsg: str
    responseToUser: str
    login: str
    currentSchedule: str
    daySchedule: str
#
# Classes for structured responses from LLM
#
class Category(BaseModel):
    category: str

class ZoomSession(BaseModel):
    login: str
    title: str

class CancelCode(BaseModel):
    code: int


class TitleURL(BaseModel):
    title: str
    url: str
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
    def __init__(self,api_key):
        api_key=api_key
        self.model=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key)
        #self.model=ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

        builder = StateGraph(AgentState)
        builder.add_node('front_end',self.frontEnd)
        builder.add_node('provide_live_schedule',self.provideLiveSchedule)
        builder.add_node('provide_matching_session',self.provideMatchingSession)
        builder.add_node('provide_cancel_code',self.provideCancelCode)
        builder.add_node('provide_zoom_link',self.provideZoomLink)

        builder.set_entry_point('front_end')
        builder.add_conditional_edges('front_end',self.main_router,
                                      {END:END, 
                                       "provide_live_schedule":"provide_live_schedule", 
                                       "provide_cancel_code":"provide_cancel_code", 
                                       "provide_zoom_link":"provide_zoom_link"})
        #builder.add_edge('provide_live_schedule',END)
        builder.add_conditional_edges('provide_live_schedule',self.second_router,
                                        {END:END, 
                                         "login_present":"provide_matching_session", 
                                         "login_absent":END})
        builder.add_edge('provide_matching_session',END)
        builder.add_edge('provide_cancel_code',END)
        builder.add_edge('provide_zoom_link',END)
        memory = SqliteSaver(conn=sqlite3.connect(":memory:", check_same_thread=False))
        self.graph = builder.compile(
            checkpointer=memory,
            # interrupt_after=['planner', 'generate', 'reflect', 'research_plan', 'research_critique']
        )
        png=self.graph.get_graph().draw_png('graph.png')
        print("Completed zoomHandler init")

    def frontEnd(self, state: AgentState):
        print(f"START: frontEnd")
        my_prompt=f"""
                Please classify the user's request.
                If the user is unable to join a Zoom session due to a conflict, category is 'Conflict'
                If the user wants you to cancel an existing Zoom session, category is 'Cancel'
                If the user expresses inability to stop a Zoom session, category is 'Cancel'
                If the user expresses the need to stop a Zoom session, category is 'Cancel'
                If the user wants you to create a new Zoom session, category is 'Create'
                Else the category is 'Other'
                """
        category=self.model.with_structured_output(Category).invoke([
            SystemMessage(content=my_prompt),
            HumanMessage(content=state['initialMsg']),
        ]).category
        #print(f"Category: {category}")
        #print(f"END: frontEnd")
        return {
            'lnode':'front_end',
            'category':category        
        }
    
    def main_router(self, state: AgentState):
        print(f"\n\nSTART: mainRouter with msg {state['initialMsg']} and category {state['category']}")
        if state['category'] == 'Conflict':
            return "provide_live_schedule"
        elif state['category'] == 'Cancel':
            return "provide_cancel_code"
        elif state['category'] == 'Create':
            return "provide_zoom_link"
        elif state['category'] == 'Other':
            print(f"Content not relevant to Zoom. Ignoring. {state['initialMsg']}")
            return END
        else:
            print(f"Unknown category {state['category']}")
            return END

    def provideLiveSchedule(self, state: AgentState):
        print(f"START: provideLiveSchedule")
        daySchedule= get_scheduled_sessions()
        # print(f"\n\n\n******\nDay Schedule: {daySchedule}\n******\n\n\n")

        my_prompt=f"""
                Please check if the user's request matches exactly one of the scheduled sessions.
                {daySchedule}
                If so, respond with the title and the login of that session.
                Else return 'No Match' for both, and we will ask user for more information.

                Please take a step-by-step approach. 
                First find the matching Title, then find the matching Login only if the Title is well-matched.
                Only provide the Title and the Login if there is a good match with exactly one session.
                Else return 'No Match' for both, and we will ask user for more information.
                """
        llm_response=self.model.with_structured_output(ZoomSession).invoke([
            SystemMessage(content=my_prompt),
            HumanMessage(content=state['initialMsg']),
        ])
        # print(f"\n\n\nLLM Response: {llm_response}\n\n\n")
        currentSchedule= get_current_sessions()
        login = llm_response.login
        if login == 'No Match':
            responseToUser= f"{currentSchedule}.\n\n\nPlease look through this list and join the appropriate session using the join_url provided."
            return {
                'lnode':'provide_live_schedule',
                'responseToUser':responseToUser,
                'daySchedule':daySchedule,
                'currentSchedule':currentSchedule,
                'login':login,
            }
    
        return {
            'lnode':'provide_live_schedule',
            'daySchedule':daySchedule,
            'currentSchedule':currentSchedule,
            'login':login,
        }
    
    def second_router(self, state: AgentState):
        print(f"\n\nSTART: secondRouter with msg {state['initialMsg']}")
        if state['login'] == 'No Match':
            return "login_absent"
        else:
            return "login_present"
        
    

    def provideMatchingSession(self, state: AgentState):
        print(f"START: provideMatchingSession")
        login=state['login']
        currentSchedule=state['currentSchedule']
        print(f"Login: {login}")
        my_second_prompt=f"""
            Please try to match the login {login} to one of the running sessions.
            {currentSchedule}
            Respond with the Title and URL of the best matching session(s).
        """
        llm_second_response=self.model.with_structured_output(TitleURL).invoke([
            SystemMessage(content=my_second_prompt),
            HumanMessage(content=state['initialMsg']),
        ])
        # print(f"\n\n\nLLM 2nd Response: {llm_second_response}\n\n\n")
        if title := llm_second_response.title:
            responseToUser= f"{currentSchedule}.\n\nI believe your conflict is with {title}\n\nPlease join this session using {llm_second_response.url}."
        else:
            responseToUser= f"{currentSchedule}.\n\nI believe your issue is with Account {login}\n\nCan you please check through the current sessions to figure out the conflict."
        return {
            'lnode':'provide_live_schedule',
            'responseToUser':responseToUser
        }

    def provideCancelCode(self, state: AgentState):
        print(f"START: provideCancelCode with msg {state['initialMsg']}")
        currentSchedule= get_current_sessions()
        zoom_table = get_zoom_table()
        my_prompt=f"""
                Please try to match the user's request to one of the running sessions.
                {currentSchedule}
                If there is no good match, return -10 as the cancel code and we will ask user for more information.

                If there is a good match, then check the Zoom table for the cancel codes. {zoom_table}
                Respond with the Code of the matching session only if there is a good match.
                Else return the Code as -100 and we will ask the user for more information.

                Please take a step-by-step approach. 
                First find the matching Host, then find the matching code only if the host is well-matched.
            """
        llm_response=self.model.with_structured_output(CancelCode).invoke([
            SystemMessage(content=my_prompt),
            HumanMessage(content=state['initialMsg']),
        ])
        print(f"LLM Response: {llm_response}")
        cancel_code=int(llm_response.code)
        if(cancel_code<0):
            responseToUser= """
            I am sorry. I could not find a match. Please provide more specifics about the session you want to cancel.\n\n
            For example, you can say: 'I want to cancel the session with the title "1:1 Maya Deren"
            """
        else:
            responseToUser= f"Please use the Host Key {cancel_code}."

        #print(f"END: provideCancelCode")
        return {
            'lnode':'provide_day_schedule',
            'responseToUser':responseToUser
        }

    def provideZoomLink(self, state: AgentState):
        print(f"START: provideZoomLink")
        responseToUser= "Sorry. I do not have the ability to create Zoom links yet. Please wait for a human to respond."
        #print(f"END: provideZoomLink")
        return {

            'lnode':'provide_zoom_link',
            'responseToUser':responseToUser
        }

