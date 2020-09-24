"""'更新模型类，给News添加了外键，'

Revision ID: 8fc0a7ac84de
Revises: 1d02ef8a3787
Create Date: 2020-09-24 09:01:23.256135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc0a7ac84de'
down_revision = '1d02ef8a3787'
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
