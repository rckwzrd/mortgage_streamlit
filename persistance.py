# https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92

import streamlit as st

#create cache object for the "chat"
# @st.cache(allow_output_mutation=True)
# def Chat():
#     return []

# chat=Chat()
# name = st.sidebar.text_input("Name")
# message = st.sidebar.text_area("Message")
# if st.sidebar.button("Post chat message"):
#     chat.append((name,message))

# if len(chat) > 10:
#     del(chat[0])

# try:
#     names, messages = zip(*chat)
#     chat1 = dict(Name = names, Message =  messages)
#     st.table(chat1)
# except ValueError:
#     st.title("Enter your name and message into the sidebar, and post!")
#     import streamlit as st
# import SessionState

import streamlit as st
import SessionState
state = SessionState.get(chat_list=[])

name = st.sidebar.text_input("Name")
message = st.sidebar.text_area("Message")
if st.sidebar.button("Post chat message"):
    state.chat_list.append((name, message))

if len(state.chat_list) > 10:
    del (state.chat_list[0])

try:
    names, messages = zip(*state.chat_list)
    chat1 = dict(Name=names, Message=messages)
    st.table(chat1)
except ValueError:
    st.title("Enter your name and message into the sidebar, and post!")