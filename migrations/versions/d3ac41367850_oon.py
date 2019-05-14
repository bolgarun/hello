"""oon

Revision ID: d3ac41367850
Revises: 41e5a8d88f5f
Create Date: 2019-05-13 15:00:24.064520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3ac41367850'
down_revision = '41e5a8d88f5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('articl_ibfk_1', 'articl', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('articl_ibfk_1', 'articl', 'user', ['user'], ['id'])
    # ### end Alembic commands ###
