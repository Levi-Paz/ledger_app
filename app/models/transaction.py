import enum
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, DECIMAL, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class TransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(DECIMAL(18, 2), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    sender_account = relationship(
        "Account",
        back_populates="sent_transactions",
        foreign_keys=[sender_account_id]
    )

    receiver_account = relationship(
        "Account",
        back_populates="received_transactions",
        foreign_keys=[receiver_account_id]
    )

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )

    def __repr__(self):
        return f"<Transaction(id={self.id}, sender_account_id={self.sender_account_id}, receiver_account_id={self.receiver_account_id}, amount={self.amount}, status='{self.status}')>"
    