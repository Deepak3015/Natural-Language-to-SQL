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

if st.button(
    "Clear Chat"
):

    st.session_state.messages = []

    st.rerun()




if "messages" not in st.session_state:

    st.session_state.messages = []




for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        if message["role"] == "user":

            st.markdown(
                message["content"]
            )

        else:

            st.subheader(
                "Generated SQL"
            )

            st.code(
                message["sql"],
                language="sql"
            )

            st.subheader(
                "Results"
            )

            st.dataframe(
                message["df"],
                use_container_width=True
            )




user_prompt = st.chat_input(
    "Ask your database..."
)




if user_prompt:



    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )



    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_prompt
        )



    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Thinking..."
        ):

            try:

                sql_query, df = ask_database(
                    user_prompt
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


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "sql": sql_query,
                        "df": df
                    }
                )

            except Exception as e:

                st.error(
                    str(e)
                )