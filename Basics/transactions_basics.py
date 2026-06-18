from fastapi import FastAPI, HTTPException, Body
import json

app = FastAPI()

with open("May_Expenses.json") as input_file:
    transactions = json.load(input_file)

@app.get("/transactions/get-transactions")
def get_transactions():
    return transactions

@app.get("/transactions/get-transactions/{transaction_date}")
def get_transactions_date(transaction_date: str):
    try:
        result = [transaction for transaction in transactions if transaction.get("Date") == transaction_date]

        return result
    
    except:
        raise HTTPException(
            status_code=404,
            detail=f"No transactions found for the date {transaction_date}"
        )

@app.get("/transactions/get-transactions/{index}")
def get_transactions(index: int):
    return transactions[index]

@app.get("/transactions/get_transactions/{category}")
async def get_category_transactions(category: str):
    try:  
        result = [transaction for transaction in transactions if transaction.get('Category') is not None and transaction.get('Category', '').casefold() == category.casefold()]
            
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No transactions found for '{category}'"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="No transactions found")

@app.post("/transactions/create-transaction")
def post_api(new_transaction = Body()):
    transactions.append(new_transaction)

@app.put("/transactions/update-transaction")
def put_api(updated_transaction = Body()):
    for i in range(len(transactions)):
        if transactions[i].get("Date") == updated_transaction.get("Date"):
            transactions[i] = updated_transaction


@app.delete("/transactions/delete-transaction/{transaction_date}")
def delete_api(transaction_date :str):
    for i in range(len(transactions)):
        if transactions[i].get("Date") == transaction_date:
            transactions.pop(i)
            break

