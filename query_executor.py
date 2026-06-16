import pandas as pd
from sqlalchemy import text
from database import engine


def execute_query(query):

    with engine.connect() as connection:

        result = connection.execute(
            text(query)
        )

        rows = []

        for row in result:

            rows.append(
                dict(row._mapping)
            )

        df = pd.DataFrame(
            rows
        )

        return df