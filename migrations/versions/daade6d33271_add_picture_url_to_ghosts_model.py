"""Add picture_url to Ghosts model

Revision ID: daade6d33271
Revises: abc31550f99e
Create Date: 2024-10-29 23:55:35.725894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daade6d33271'
down_revision = 'abc31550f99e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ghostbusters', schema=None) as batch_op:
        batch_op.drop_column('picture_url')

    with op.batch_alter_table('ghosts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_url', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ghosts', schema=None) as batch_op:
        batch_op.drop_column('picture_url')

    with op.batch_alter_table('ghostbusters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_url', sa.VARCHAR(length=255), nullable=True))

    # ### end Alembic commands ###