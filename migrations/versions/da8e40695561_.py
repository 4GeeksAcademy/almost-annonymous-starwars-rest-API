"""empty message

Revision ID: da8e40695561
Revises: 0a0533d1f8bc
Create Date: 2025-06-17 23:19:57.442573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da8e40695561'
down_revision = '0a0533d1f8bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_characters', schema=None) as batch_op:
        batch_op.drop_constraint('favorite_characters_user_id_key', type_='unique')

    with op.batch_alter_table('favorite_planets', schema=None) as batch_op:
        batch_op.drop_constraint('favorite_planets_user_id_key', type_='unique')

    with op.batch_alter_table('favorite_vehicles', schema=None) as batch_op:
        batch_op.drop_constraint('favorite_vehicles_user_id_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_vehicles', schema=None) as batch_op:
        batch_op.create_unique_constraint('favorite_vehicles_user_id_key', ['user_id'])

    with op.batch_alter_table('favorite_planets', schema=None) as batch_op:
        batch_op.create_unique_constraint('favorite_planets_user_id_key', ['user_id'])

    with op.batch_alter_table('favorite_characters', schema=None) as batch_op:
        batch_op.create_unique_constraint('favorite_characters_user_id_key', ['user_id'])

    # ### end Alembic commands ###
