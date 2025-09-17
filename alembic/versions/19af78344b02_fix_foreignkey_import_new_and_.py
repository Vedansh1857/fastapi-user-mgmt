"""Fix ForeignKey import new and relationship

Revision ID: 19af78344b02
Revises: 539d06ff7999
Create Date: 2025-09-17 15:28:05.286563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '19af78344b02'
down_revision: Union[str, Sequence[str], None] = '539d06ff7999'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'coach_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('expertise', sa.String(length=255), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('availability', sa.Enum('available', 'unavailable', name='availabilityenum'), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),  # ForeignKey constraint
        sa.PrimaryKeyConstraint('id'),
        mysql_collate='utf8mb4_0900_ai_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )

def downgrade() -> None:
    op.drop_table('coach_profiles')
