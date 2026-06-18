class Transaction:

    transaction_id: int
    transaction_date: str
    description: str
    category: str
    debit_account: str

    def __init__(self, transaction_id, transaction_date, description, category, debit_account):
        self.transaction_id = transaction_id
        self.transaction_date = transaction_date
        self.description = description
        self.category = category
        self.debit_account = debit_account