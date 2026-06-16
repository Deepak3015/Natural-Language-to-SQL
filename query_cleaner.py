def clean_sql(sql):

    unwanted_words = [
        "```sql",
        "```",
        "SQL:"
    ]

    for word in unwanted_words:

        sql = sql.replace(
            word,
            ""
        )

    return sql.strip()