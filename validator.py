def check_validation(sql):

    dangerous_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE"
    ]

    sql_upper = sql.upper()

    for keyword in dangerous_keywords:

        if keyword in sql_upper:

            raise Exception(
                f"{keyword} statements are not allowed."
            )

    return True