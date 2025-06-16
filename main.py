import os
from fastapi import FastAPI
from models import ChatRequest, ChatResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Api is running"}
