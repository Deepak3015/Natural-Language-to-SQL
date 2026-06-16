def check_validation(query):
    restrict_word = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE"
    ]
    query_upper = query.upper()

    for keyword in restrict_word :
        if keyword in query_upper:
            raise  ValueError(f"{keyword} queries are not allowed.")
    
    return True


