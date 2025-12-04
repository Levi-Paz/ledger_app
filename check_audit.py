import asyncio
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.audit_log import AuditLog

async def check_audit_logs():
    async with SessionLocal() as db:
        print("\n🕵️  VERIFICANDO LOGS DE AUDITORIA (SQL TRIGGER)...")
        print("-" * 60)
        
        stmt = select(AuditLog).order_by(AuditLog.date_action.desc()).limit(5)
        result = await db.execute(stmt)
        logs = result.scalars().all()

        if not logs:
            print("Nenhum log encontrado. Você fez alguma transferência DEPOIS de criar a trigger?")
        
        for log in logs:
            print(f"🕒 [{log.date_action}] Ação: {log.action} na Tabela: {log.table_name} (ID {log.record_id})")
            print(f" 🔻 Antes: {log.old_values}")
            print(f" 🔺 Depois: {log.new_values}")
            print("-" * 60)

if __name__ == "__main__":
    asyncio.run(check_audit_logs())
