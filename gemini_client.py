import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = key )
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_sql(prompt):

    response = model.generate_content(
        prompt
    )

    return response.text

def clean_sql(sql):

    sql = re.sub(
        r"```.*?\n",
        "",
        sql
    )

    sql = sql.replace(
        "```",
        ""
    )

    return sql.strip()