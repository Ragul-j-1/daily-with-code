from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI(title="Personal Expenses Tracker")


def create_table():
    try:
        con = sqlite3.connect("personal_expenses_tracker.db")
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                amount FLOAT
            )
        """)
        con.commit()
    except Exception as e:
        print("Error creating table:", e)
    finally:
        con.close()

create_table()


class Expense(BaseModel):
    cat: str
    amt: float
    
@app.get("/display")
def get_data():
    try:
        con = sqlite3.connect("personal_expenses_tracker.db")
        cur = con.cursor()
        cur.execute("SELECT category, amount FROM expenses")
        rows = cur.fetchall()
        return {"expenses": [{"category": r[0], "amount": r[1]} for r in rows]}
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()


@app.post("/insert")
def add_data(data: List[Expense]):
    try:
        con = sqlite3.connect("personal_expenses_tracker.db")
        cur = con.cursor()
        for exp in data:
            cur.execute(
                "INSERT OR REPLACE INTO expenses(category, amount) VALUES (?, ?)",
                (exp.cat, exp.amt)
            )
        con.commit()
        return {"message": f"{len(data)} expense(s) added/updated successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()





@app.put("/update")
def update_expense(data: Expense):
    try:
        con = sqlite3.connect("personal_expenses_tracker.db")
        cur = con.cursor()
        cur.execute("UPDATE expenses SET amount=? WHERE category=?", (data.amt, data.cat))
        con.commit()
        updated = cur.rowcount
        if updated == 0:
            return {"message": f"No expense found with category '{data.cat}'"}
        return {"message": f"{updated} record(s) updated successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()
        
@app.delete("/delete/{category}")
def delete_expense(category: str):
    try:
        con = sqlite3.connect("personal_expenses_tracker.db")
        cur = con.cursor()
        cur.execute("DELETE FROM expenses WHERE category = ?", (category,))
        con.commit()
        deleted = cur.rowcount  # how many rows deleted
        if deleted == 0:
            return {"message": f"No expense found with category '{category}'"}
        return {"message": f"{deleted} expense(s) deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()
