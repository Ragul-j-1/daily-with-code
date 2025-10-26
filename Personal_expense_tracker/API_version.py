from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Input(BaseModel):
    category: str
    amount: int

personal = []
expenses = {}

@app.get("/display")
async def display():
    return personal

@app.post("/insert")
async def insert_data(data: List[Input]):
    for item in data:
        expenses[item.category] = item.amount
        personal.append({item.category: item.amount})
    return {"message": "Multiple data inserted successfully", "expenses": expenses}
