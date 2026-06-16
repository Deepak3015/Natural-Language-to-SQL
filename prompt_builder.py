def build_prompt(schema, user_question):

    schema_text = ""

    for table, columns in schema.items():

        schema_text += f"\n{table}\n(\n"
        schema_text += ",\n".join(columns)
        schema_text += "\n)\n"

    prompt = f"""
You are an expert MySQL developer.

Database Schema:

{schema_text}

User Question:

{user_question}

Rules:

1. Generate MySQL queries only.
2. Return only SQL.
3. Never explain.
4. Never use markdown.
5. Never use ```sql.
6. Use only tables present in schema.
7. Generate one query only.

SQL:
"""

    return prompt