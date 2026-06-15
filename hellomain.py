"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/about")
def about_root():
    return {'message' : 'This is for educational purpose'}
"""