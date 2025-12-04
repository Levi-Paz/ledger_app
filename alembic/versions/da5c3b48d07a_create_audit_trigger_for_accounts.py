"""create audit trigger for accounts

Revision ID: da5c3b48d07a
Revises: 4255db478fb4
Create Date: 2025-11-28 20:25:44.223803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da5c3b48d07a'
down_revision: Union[str, Sequence[str], None] = '4255db478fb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TRIGGER trg_AuditAccounts_BalanceUpdate
    ON accounts
    AFTER UPDATE
    AS
    BEGIN
        SET NOCOUNT ON;
        IF UPDATE(balance)
        BEGIN
            INSERT INTO audit_logs (
                table_name, 
                record_id, 
                action, 
                old_values, 
                new_values, 
                date_action
            )
            SELECT 
                'accounts',
                i.id,
                'UPDATE',
                (SELECT d.balance FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                (SELECT i.balance FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
                GETUTCDATE()
            FROM inserted i
            JOIN deleted d ON i.id = d.id;
        END
    END
    """)


def downgrade() -> None:
    # Se precisarmos desfazer a migração, apagamos a trigger
    op.execute("DROP TRIGGER IF EXISTS trg_AuditAccounts_BalanceUpdate")
