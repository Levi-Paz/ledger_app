from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.transaction import TransferRequest, TransferResponse, StatementItem, StatementResponse
from app.repositories.ledger_repo import LedgerRepository
from app.services.transfer_service import TransferService


router = APIRouter()

@router.post(
        "/transfer",
        response_model=TransferResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Realiza uma transferência entre duas contas",
        description="Executa uma transação ACID. Aplica Row Locking nas contas, valida saldo e gera histórico atomicamente."
        )
async def transfer_money(
    request: TransferRequest,
    db: AsyncSession = Depends(get_db)
    ):
    try:
        repo = LedgerRepository(db)
        service = TransferService(repo)
        response = await service.execute_transfer(request)

        await db.commit()

        return response
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    

@router.get(
        "/statement/{account_id}",
        response_model=StatementResponse,
        summary="Obtém o extrato detalhado de uma conta",
        description="Utiliza window functions do SQL Server para calcular o saldo acumulado linha a linha."
        )
async def get_account_statement(
    account_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    repo = LedgerRepository(db)
    current_balance = await repo.get_account_balance(account_id)
    raw_txs = await repo.get_statement(account_id)
    statements_items = []
    for row in raw_txs:
        item = StatementItem(
            transaction_id=row.id,
            amount=row.amount,
            type=row.type,
            balance_after=row.balance_after,
            created_at=row.created_at,
            other_party_account_id=(row.sender_account_id if row.type == 'credit' else row.receiver_account_id)
        )
        statements_items.append(item)

    return StatementResponse(
        account_id=account_id,
        current_balance=current_balance,
        transactions=statements_items
    )
