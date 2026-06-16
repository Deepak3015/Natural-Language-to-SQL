import streamlit as st
from sql_agent import ask_database

st.set_page_config(
    page_title="SQLMind AI",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 SQLMind AI"
)

user_prompt = st.text_input(
    "Ask your database"
)

if st.button(
    "Submit"
) and user_prompt:

    with st.spinner(
        "Thinking..."
    ):

        try:

            sql_query, df = ask_database(
                user_prompt
            )

            st.success(
                "Query executed successfully!"
            )

            st.subheader(
                "Generated SQL"
            )

            st.code(
                sql_query,
                language="sql"
            )

            st.subheader(
                "Results"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:

            st.error(
                str(e)
            )