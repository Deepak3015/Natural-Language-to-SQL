from schema_loader import get_schema
from prompt_builder import built_prompt
from gemini_client import generate_sql, clean_sql
from query_executor import execute_query
from validator import check_validation

question1 = "Show all customers"
question2 = "Delete all customers"

schema = get_schema()

prompt = built_prompt(
    schema,
    question2
)

print("Prompt:")
print(prompt)


generated_sql = generate_sql(
    prompt
)

print("\nGenerated SQL:")
print(generated_sql)


cleaned_sql = clean_sql(
    generated_sql
)

print("\nCleaned SQL:")
print(cleaned_sql)

check_validation(cleaned_sql)


df = execute_query(
    cleaned_sql
)

print("\nResult:")
print(df)