from schema_loader import get_schema
from prompt_builder import build_prompt
from llm import generate_sql
from query_cleaner import clean_sql
from validator import check_validation
from query_executor import execute_query

schema = get_schema()

tests = [
    "Show all employees and their department names",
    "List all products with their category names",
    "Show all orders with customer names and payment status",
]

for question in tests:
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"Q: {question}")
    prompt = build_prompt(schema, question)
    sql = generate_sql(prompt)
    cleaned = clean_sql(sql)
    print(f"SQL: {cleaned}")
    check_validation(cleaned)
    df = execute_query(cleaned)
    print(f"Rows: {len(df)}")
    if len(df) > 0:
        print(df.head(3).to_string())
    else:
        print("(empty result)")
