from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, case, func
from sqlalchemy.orm import aliased
from app.models.account import Account
from app.models.transaction import Transaction, TransactionStatus
from decimal import Decimal

class LedgerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_account_for_update(self, account_id: int) -> Account | None:
        """
        Busca uma conta e aplica o ROWLOCK para evitar condições de corrida.
        """
        stmt = select(Account).where(Account.id == account_id).with_for_update()
        result = await self.db.execute(stmt)
        return result.scalars().first()
    

    async def create_transaction_record(self, 
                                        sender_account_id: int, 
                                        receiver_account_id: int, 
                                        amount: Decimal
                                        ) -> Transaction:
        tx = Transaction(
            sender_account_id=sender_account_id,
            receiver_account_id=receiver_account_id,
            amount=amount,
            status=TransactionStatus.COMPLETED
        )
        self.db.add(tx)
        await self.db.flush()
        return tx


    async def get_statement(self, account_id: int):
        signed_amount = case(
            (Transaction.receiver_account_id == account_id, Transaction.amount),
            else_=-Transaction.amount
            )
        
        stmt = select(
            Transaction.id,
            Transaction.amount,
            Transaction.sender_account_id,
            Transaction.receiver_account_id,
            Transaction.created_at,
            case(
                (Transaction.receiver_account_id == account_id, 'credit'),
                else_='debit'
            ).label('type'),
            func.sum(signed_amount).over(
                order_by=[Transaction.created_at, Transaction.id]
            ).label('balance_after')
        ).where(
            or_(Transaction.sender_account_id == account_id, Transaction.receiver_account_id == account_id)
        ).order_by(
            Transaction.created_at.asc()
        )

        result = await self.db.execute(stmt)
        return result.all()
    
    
    async def get_account_balance(self, account_id: int) -> Decimal | None:
        stmt = select(Account.balance).where(Account.id == account_id)
        result = await self.db.execute(stmt)
        val = result.scalar()
        return val if val is not None else Decimal(0)
    