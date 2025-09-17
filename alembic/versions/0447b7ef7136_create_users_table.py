"""Create users table

Revision ID: 0447b7ef7136
Revises: 
Create Date: 2025-09-17 13:03:38.361834

"""
from typing import Sequence, Union
import enum

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0447b7ef7136'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Enum to define the roles
class RoleEnum(str, enum.Enum):
    coach = "coach"
    coachee = "coachee"

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum(RoleEnum), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
