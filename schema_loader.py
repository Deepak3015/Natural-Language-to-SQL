from sqlalchemy import inspect
from database import engine


def get_schema():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    schema = {}

    for table in tables:

        columns = inspector.get_columns(table)

        schema[table] = []

        for column in columns:

            schema[table].append(
                column["name"]
            )

    return schema