from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from typing import List
app=FastAPI()

def create_table():
    con = sqlite3.connect("personal_expenses_tracker.db")
    cur = con.cursor()
    cur.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    category TEXT,amount FLOAT)""")
    con.commit()
    con.close()
create_table()

class expe(BaseModel):
    cat:str
    amt:float
    
@app.post("/insert")
def add_data(data:List[expe]):
    con = sqlite3.connect("personal_expenses_tracker.db")
    cur = con.cursor()
    for s in data:
        cur.execute("INSERT INTO expenses(category,amount) VALUES (?,?)",(s.cat,s.amt))
        con.commit()
        con.close()
        return {"message": f"{len(data)} students added successfully"}
print("table created amnd inserted")
@app.get("/display")
def get_data():
    con = sqlite3.connect("personal_expenses_tracker.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM expenses")
    rows=cur.fetchall()
    con.close()
    return {"expenses": rows}
@app.put("/update")
def update(data:expe):
    con = sqlite3.connect("personal_expenses_tracker.db")
    cur = con.cursor()
    cur.execute("UPDATE expenses amount=? WHERE category=?",(data.amt,data.cat))
    con.commit()
    con.close()
    return{"the data is updated"}
    
    
    

















