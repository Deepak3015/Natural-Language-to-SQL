import streamlit as st
from sql_agent import ask_database

st.title(
    "SQLMind AI"
)

user_prompt = st.text_input("Ask me anything")
if st.button("Submit"):

    with st.spinner(
        "Thinking..."
    ):

        try:

            df = ask_database(
                user_prompt
            )

            st.dataframe(
                df
            )

        except Exception as e:

            st.error(
                str(e)
            )
