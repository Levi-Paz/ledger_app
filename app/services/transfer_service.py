from fastapi import HTTPException
from app.repositories.ledger_repo import LedgerRepository
from app.schemas.transaction import TransferRequest, TransferResponse


class TransferService:
    def __init__(self, repo: LedgerRepository):
        self.repo = repo

    async def execute_transfer(self, data: TransferRequest) -> TransferResponse:
        # Busca as contas com lock para evitar condições de corrida

        if data.sender_account_id == data.receiver_account_id:
            raise HTTPException(status_code=400, detail="Remetente e destinatário não podem ser a mesma conta.")
        
        first_id, second_id = sorted([data.sender_account_id, data.receiver_account_id])

        account_1 = await self.repo.get_account_for_update(first_id)
        account_2 = await self.repo.get_account_for_update(second_id)

        sender = account_1 if account_1.id == data.sender_account_id else account_2
        receiver = account_1 if account_1.id == data.receiver_account_id else account_2

        if not sender or not receiver:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")
        
        if sender.balance < data.amount:
            raise HTTPException(status_code=400, detail="Saldo insuficiente na conta do remetente.")
        
        sender.balance -= data.amount
        receiver.balance += data.amount 

        tx = await self.repo.create_transaction_record(
            sender_account_id=sender.id,
            receiver_account_id=receiver.id,
            amount=data.amount
        )

        return TransferResponse(
            transaction_id=tx.id,
            sender_balance=sender.balance,
            receiver_balance=receiver.balance,
            status="COMPLETED"
        )
