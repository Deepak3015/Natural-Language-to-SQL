from sqlalchemy import text
import pandas as pd
from database import engine





def execute_query(query):
    try:
            with engine.connect() as connection:

                print("Connected successfully!")
                query =  text("Select * from customer")
                result = connection.execute(query)
                rows = []
                for row in result:
                    rows.append(dict(row._mapping))
                df = pd.DataFrame(rows)
            return df
    except Exception as e:
        raise e