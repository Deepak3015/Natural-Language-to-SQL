def built_prompt(schema,query):
    schema_text = ""

    for table, columns in schema.items():
        schema_text += f"\n{table}\n(\n"
        schema_text += ",\n".join(columns)
        schema_text += "\n)\n"
    prompt = f"""
You are an expert SQL developer.

Database Schema:

{schema_text}

User Question:

{query}

Generate only SQL query.
Do not explain anything.
Return only SQL.
"""