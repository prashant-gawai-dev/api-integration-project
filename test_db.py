from database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("connected successfully")
        print(result)
except Exception as e:
    print("connection failed")
    print(e)
