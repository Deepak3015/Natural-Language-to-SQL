import streamlit as st
import pandas as pd
from llm import generate_sql
import json


def suggest_visualizaion(question, df):

    sample = df.head(10).to_string(index=False)

    prompt = f"""
Question: {question}

Columns: {list(df.columns)}

Sample Data:
{sample}

Available Charts: metric, card, bar, line, pie, table

Return ONLY this JSON format:
{{"chart_type": "bar", "title": "short title", "insight": "one sentence insight"}}

Use these exact keys: chart_type, title, insight
"""

    response = generate_sql(prompt)
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    return json.loads(response)


def visualize(suggestion, df):

    chart_type = suggestion.get("chart_type", "table")
    title = suggestion.get("title", "Chart")
    insight = suggestion.get("insight", "")

    st.subheader(title)

    chart_df = df.set_index(df.columns[0])

    if chart_type == "bar":
        st.bar_chart(chart_df)
    elif chart_type == "line":
        st.line_chart(chart_df)
    elif chart_type == "metric":
        st.metric(label=df.columns[0], value=round(df.iloc[0, 0], 2))
    elif chart_type == "table":
        st.dataframe(df, hide_index=True)

    if insight:
        st.success(insight)
