"""Making table fields

Revision ID: 57b616290d5e
Revises: e391725dff70
Create Date: 2024-03-27 09:43:22.297649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57b616290d5e'
down_revision: Union[str, None] = 'e391725dff70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('messages', sa.Column('message', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('prompt', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('message_type', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('messages', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'messages', 'users', ['user_id'], ['id'])
    op.add_column('readings', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('readings', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('readings', sa.Column('humidity', sa.Float(), nullable=True))
    op.add_column('readings', sa.Column('pH', sa.Float(), nullable=True))
    op.add_column('readings', sa.Column('nitrogen', sa.Float(), nullable=True))
    op.add_column('readings', sa.Column('phosphorus', sa.Float(), nullable=True))
    op.add_column('readings', sa.Column('potassium', sa.Float(), nullable=True))
    op.add_column('readings', sa.Column('temperature', sa.Float(), nullable=True))
    op.add_column('readings', sa.Column('rainfall', sa.Float(), nullable=True))
    op.add_column('readings', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('readings', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'readings', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(), nullable=True))
    op.add_column('users', sa.Column('country', sa.String(), nullable=True))
    op.add_column('users', sa.Column('language', sa.String(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'language')
    op.drop_column('users', 'country')
    op.drop_column('users', 'city')
    op.drop_column('users', 'phone')
    op.drop_column('users', 'name')
    op.drop_column('users', 'address')
    op.drop_constraint(None, 'readings', type_='foreignkey')
    op.drop_column('readings', 'updated_at')
    op.drop_column('readings', 'created_at')
    op.drop_column('readings', 'rainfall')
    op.drop_column('readings', 'temperature')
    op.drop_column('readings', 'potassium')
    op.drop_column('readings', 'phosphorus')
    op.drop_column('readings', 'nitrogen')
    op.drop_column('readings', 'pH')
    op.drop_column('readings', 'humidity')
    op.drop_column('readings', 'timestamp')
    op.drop_column('readings', 'user_id')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'updated_at')
    op.drop_column('messages', 'created_at')
    op.drop_column('messages', 'message_type')
    op.drop_column('messages', 'prompt')
    op.drop_column('messages', 'message')
    op.drop_column('messages', 'user_id')
    # ### end Alembic commands ###
