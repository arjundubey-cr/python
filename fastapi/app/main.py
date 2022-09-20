from fastapi import FastAPI, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
import models
from database import engine
from routes import post, user
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Connecting to the database
# Try to reconnect to the database every 2sec until the success
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='Arjun@2001', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print(f'Error: {error}')
#         time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Server is up and running"}
