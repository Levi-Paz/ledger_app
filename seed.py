import asyncio
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.account import Account

async def seed_database():
    print("🌱 Iniciando o seed do banco de dados...")

    async with SessionLocal() as db:
        stmt =  select(Account).limit(1)
        result = await db.execute(stmt)
        account = result.scalars().first()
        if account:
            print("✅ Conta já existe. Seed não é necessário.")
            return
        jhow = Account(name="jhow", balance=1000)
        brow = Account(name="brow", balance=100)

        db.add_all([jhow, brow])
        await db.commit()

        await db.refresh(jhow)
        await db.refresh(brow)

        print("\n✅ Sucesso! Contas criadas:")
        print("-" * 80)
        print(f"👤 ID: {jhow.id} | Nome: {jhow.name} | Saldo: R$ {jhow.balance}")
        print("-" * 80)
        print(f"👤 ID: {brow.id} | Nome: {brow.name} | Saldo: R$ {brow.balance}")
        print("-" * 80)
        print("Agora você pode usar esses IDs para testar a transferência via API.")

if __name__ == "__main__":
    asyncio.run(seed_database())
    