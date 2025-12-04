from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(100), nullable=False) # 'accounts', 'transactions'
    record_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)  # 'INSERT', 'UPDATE', 'DELETE'
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    date_action = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AuditLog(id={self.id}, table_name='{self.table_name}', action='{self.action}')>"
    