import streamlit as st
from record_page import record_page
from list_and_chat_page import list_and_chat_page

page = st.sidebar.radio("Menu", ["Gravar Áudio", "Listar Áudios e Chat"])

if page == "Gravar Áudio":
    record_page()
elif page == "Listar Áudios e Chat":
    list_and_chat_page()
