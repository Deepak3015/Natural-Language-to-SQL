from schema_loader import get_schema
from prompt_builder import built_prompt
from gemini_client import generate_sql, clean_sql
from query_executor import execute_query
from validator import check_validation


def ask_databse(input): 

        schema = get_schema()

        prompt = built_prompt(
            schema,
            input
        )

        generated_sql = generate_sql(
            prompt
        )

        cleaned_sql = clean_sql(
            generated_sql
        )

        check_validation(cleaned_sql)


        df = execute_query(
            cleaned_sql
        )
        print("Generated SQL:")
        print(generated_sql)

        print("Cleaned SQL:")
        print(cleaned_sql)
        return df
