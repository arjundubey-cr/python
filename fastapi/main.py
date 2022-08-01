from fastapi import FastAPI

app = FastAPI()


# async keyword is needed if you're calling any asynchronus API
# The decorator allows to modify the behaviour of a function or class.
@app.get("/")
def root():
    return {"message": "Hello World"}
