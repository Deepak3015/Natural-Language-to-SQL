from query_executor import execute_query
from schema_loader import get_schema

query = "Select * from product"

result = execute_query(query)
schema  = get_schema()
print(schema)
# print(result)





