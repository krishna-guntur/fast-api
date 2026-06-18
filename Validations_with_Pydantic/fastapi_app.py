from fastapi import FastAPI, Body, HTTPException
from transactions import Transaction
from transactionRequest import TransactionRequest

transactions = [Transaction(1, '18-06-2026', 100, 'Testing FastAPI', 'Development', 'Time'),
                Transaction(2, '19-06-2026', 95, 'Learning FastAPI', 'Development', ''),
                Transaction(3, '20-06-2026', 189, 'Applying FastAPI', 'Development', 'Time'),
                Transaction(4, '21-06-2026', 22009, 'All FastAPI', 'Development', ''),
                Transaction(5, '22-06-2026', 15008, 'Important FastAPI', 'Development', ''),
                Transaction(6, '23-06-2026', 14526, 'Glue FastAPI', 'Development', 'Time'),
                Transaction(7, '24-06-2026', 2, 'Everything FastAPI', 'Development', 'Time')
                ]


app = FastAPI()

@app.get("/transactions/get-all-transactions")
def get_all_transactions():
    return transactions

@app.post("/transactions/create-transaction")
def create_transaction(new_transaction : TransactionRequest):
    new_main_transaction = Transaction(
    **new_transaction.model_dump()
        )
    new_main_transaction.transaction_id = len(transactions)+1 if new_main_transaction.transaction_id == None else new_main_transaction.transaction_id
    transactions.append(new_main_transaction)