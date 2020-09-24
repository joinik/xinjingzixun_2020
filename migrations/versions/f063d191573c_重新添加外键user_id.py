"""'重新添加外键user_id'

Revision ID: f063d191573c
Revises: 8fc0a7ac84de
Create Date: 2020-09-24 14:41:22.664411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f063d191573c'
down_revision = '8fc0a7ac84de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'news', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'news', type_='foreignkey')
    op.drop_column('news', 'user_id')
    # ### end Alembic commands ###
