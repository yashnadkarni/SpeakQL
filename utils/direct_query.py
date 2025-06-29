import streamlit as st
from langchain_community.utilities import SQLDatabase
import pandas as pd


db = SQLDatabase.from_uri(st.session_state.db_uri)

st.title('Direct Query')


st.write(f'Dialect: {db.dialect}')
st.write(f'Tables present: {db.get_usable_table_names()}')
#print(db.run("SELECT * FROM Artist LIMIT 10;"))

if prompt := st.chat_input("Enter your query"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(db.run(prompt))
