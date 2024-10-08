"""Initial migration

Revision ID: 3290fac8ce15
Revises: 
Create Date: 2024-09-25 16:24:44.638984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3290fac8ce15'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(length=254), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('avatar', sa.String(length=254), nullable=True),
    sa.Column('refresh_token', sa.String(length=1024), nullable=True),
    sa.Column('is_email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('is_password_valid', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('contacts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(length=254), nullable=False),
    sa.Column('last_name', sa.String(length=254), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=True),
    sa.Column('phone', sa.String(length=38), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('address', sa.String(length=254), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'email', name='uix_email'),
    sa.UniqueConstraint('user_id', 'phone', name='uix_phone')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts')
    op.drop_table('users')
    # ### end Alembic commands ###
