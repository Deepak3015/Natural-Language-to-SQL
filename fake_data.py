from faker import Faker
import random
import pandas as pd

fake = Faker("en_IN")
customer = []

for i in range (1000):
    customer.append({
        "first_name":fake.first_name(),
        "last_name": fake.last_name(),
        "gender": random.choice(["Male","Female"]),
        "age":random.randint(18,60),
        "email":fake.email(),
        "phone" : fake.phone_number(),
        "city":fake.city(),
        "state":fake.state(),
        "country":"India",
        "sign_up_date":fake.date_between("-3y","today"),
        "loyalty_points":random.randint(0,5000)})
    
customer_df = pd.DataFrame(customer)

print(customer_df)
