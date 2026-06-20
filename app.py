import streamlit as st
from datetime import datetime
from visualize import visualize
from sql_agent import ask_database
from schema_loader import get_schema


st.set_page_config(
    page_title="SQLMind AI",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 SQLMind AI"
)


if "messages" not in st.session_state:

    st.session_state.messages = []


if "history" not in st.session_state:

    st.session_state.history = []



schema = get_schema()

with st.sidebar:

    st.header(
        "⚙️ SQLMind AI"
    )

    st.write(
        "Model : Qwen2.5:3b"
    )

    st.write(
        "Database : MySQL"
    )

    st.write(
        f"Tables : {len(schema)}"
    )

    st.subheader(
        "Tables"
    )

    for table in schema:

        st.write(
            f"📄 {table}"
        )

    st.divider()

    st.subheader(
        "Database Schema"
    )

    st.json(
        schema
    )

    st.divider()

    st.subheader(
        "🕒 Query History"
    )

    for item in reversed(
        st.session_state.history
    ):

        with st.expander(
            item["question"]
        ):

            st.caption(
                item["time"]
            )

            st.code(
                item["sql"],
                language="sql"
            )

    st.divider()

    if st.button(
        "🗑 Clear Chat"
    ):

        st.session_state.messages = []

        st.session_state.history = []

        st.rerun()



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

    # Store User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Display User Message

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_prompt
        )

    # Assistant Response

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

                # Save Query History

                st.session_state.history.append(
                    {
                        "question": user_prompt,
                        "sql": sql_query,
                        "time": datetime.now().strftime(
                            "%H:%M:%S"
                        )
                    }
                )

                # Display SQL

                st.subheader(
                    "Generated SQL"
                )

                st.code(
                    sql_query,
                    language="sql"
                )

                # Display Data

                visualize(df)

                # Store Assistant Message

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
