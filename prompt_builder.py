def built_prompt(schema,user_question):
    schema_text = ""

    for table, columns in schema.items():
        schema_text += f"\n{table}\n(\n"
        schema_text += ",\n".join(columns)
        schema_text += "\n)\n"

    prompt = prompt = f"""
        You are an expert MySQL developer.

        Database Schema:

        {schema}

        User Question:

        {user_question}

        Rules:

        1. Generate MySQL queries only.
        2. Return only SQL.
        3. Use only tables present in the schema.
        4. Do not use system tables.
        5. When querying metadata, restrict results to DATABASE().

        """
    return prompt
    