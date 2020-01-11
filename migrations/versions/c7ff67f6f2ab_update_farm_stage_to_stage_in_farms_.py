"""Update farm_stage to stage in farms table

Revision ID: c7ff67f6f2ab
Revises: ed68a1804aed
Create Date: 2020-01-11 20:03:07.730677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ff67f6f2ab'
down_revision = 'ed68a1804aed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('farms', sa.Column('stage', sa.String(length=64), nullable=True))
    op.drop_column('farms', 'farm_stage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('farms', sa.Column('farm_stage', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column('farms', 'stage')
    # ### end Alembic commands ###
