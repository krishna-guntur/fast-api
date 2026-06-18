from fastapi import FastAPI, Body, HTTPException
from transactions import Transaction

transactions = [Transaction(1, '18-06-2026', 'Testing FastAPI', 'Development', 'Time'),
                Transaction(2, '19-06-2026', 'Learning FastAPI', 'Development', ''),
                Transaction(3, '20-06-2026', 'Applying FastAPI', 'Development', 'Time'),
                Transaction(4, '21-06-2026', 'All FastAPI', 'Development', ''),
                Transaction(5, '22-06-2026', 'Important FastAPI', 'Development', ''),
                Transaction(6, '23-06-2026', 'Glue FastAPI', 'Development', 'Time'),
                Transaction(7, '24-06-2026', 'Everything FastAPI', 'Development', 'Time'),
                ]


app = FastAPI()

@app.get("/transactions/get-all-transactions")
def get_all_transactions():
    return transactions

@app.post("/transactions/create-transaction")
def create_transaction(new_transaction = Body()):
    transactions.append(new_transaction)