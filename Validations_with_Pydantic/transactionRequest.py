from pydantic import BaseModel, Field
from typing import Optional

class TransactionRequest(BaseModel):

    transaction_id: int = Field(description='ID is not needed for POST requests.', default=None)
    transaction_date: str = Field(pattern=r"^(0?[1-9]|[12][0-9]|3[01])-(0?[1-9]|1[0-2])-\d{2}$")
    amount: float
    description: str
    category: str
    debit_account:str

    