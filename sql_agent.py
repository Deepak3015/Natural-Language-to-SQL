from schema_loader import get_schema
from prompt_builder import build_prompt
from llm import generate_sql
from query_cleaner import clean_sql
from validator import check_validation
from query_executor import execute_query


def ask_database(user_question):

    schema = get_schema()

    prompt = build_prompt(
        schema,
        user_question
    )

    generated_sql = generate_sql(
        prompt
    )

    cleaned_sql = clean_sql(
        generated_sql
    )

    check_validation(
        cleaned_sql
    )

    df = execute_query(
        cleaned_sql
    )

    return cleaned_sql, df