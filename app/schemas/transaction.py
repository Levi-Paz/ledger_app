from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List
from datetime import datetime

class TransferRequest(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal = Field(..., gt=0, description="Valor a ser transferido deve ser positivo")

class TransferResponse(BaseModel):
    transaction_id: int
    sender_balance: Decimal
    receiver_balance: Decimal
    status: str

class StatementItem(BaseModel):
    transaction_id: int
    amount: Decimal
    type: str 
    balance_after: Decimal
    created_at: datetime
    other_party_account_id: int | None

class StatementResponse(BaseModel):
    account_id: int
    current_balance: Decimal
    transactions: List[StatementItem]
