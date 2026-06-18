from pydantic import BaseModel, Field

class TransactionRequest(BaseModel):

    transaction_id: int
    transaction_date: str = Field(pattern=r"^(0?[1-9]|[12][0-9]|3[01])-(0?[1-9]|1[0-2])-\d{2}$")
    amount: float
    description: str
    category: str
    debit_account:str

    