import streamlit as st
from record_page import record_page
from list_and_chat_page import list_and_chat_page
from streamlit_option_menu import option_menu

page = st.sidebar.radio("Ir para", ["Gravar Áudio", "Listar Áudios e Chat"])

if page == "Gravar Áudio":
    record_page()
elif page == "Listar Áudios e Chat":
    list_and_chat_page()
