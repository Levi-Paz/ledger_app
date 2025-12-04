import asyncio
from sqlalchemy import inspect
from app.core.database import engine

async def verify_tables():
    print("🔌 Conectando ao SQL Server...")
    
    async with engine.connect() as conn:
        # O 'inspect' é síncrono, então usamos run_sync para rodá-lo dentro do async
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
        
        print(f"\n✅ Conexão bem sucedida! Encontrei {len(tables)} tabelas:")
        print("-" * 30)
        for table in tables:
            print(f" 📦 {table}")
        print("-" * 30)

        # Verificação extra: Se as tabelas certas estão lá
        expected = {"accounts", "transactions", "audit_logs", "alembic_version"}
        found = set(tables)
        
        if expected.issubset(found):
            print("\n🚀 Tudo pronto! O banco está estruturado corretamente.")
        else:
            missing = expected - found
            print(f"\n⚠️ FALTAM TABELAS: {missing}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(verify_tables())