

from sql_agent import ask_databse

user_query = input("Ask me Anything........")

df = ask_databse(user_query)
print(df)