from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    balance = Column(DECIMAL(18, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sent_transactions = relationship(
        "Transaction",
        back_populates="sender_account",
        foreign_keys='Transaction.sender_account_id'
        )

    received_transactions = relationship(
        "Transaction",
        back_populates="receiver_account",
        foreign_keys='Transaction.receiver_account_id'
        )

    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_non_negative'),
    )

    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', balance={self.balance})>"
    