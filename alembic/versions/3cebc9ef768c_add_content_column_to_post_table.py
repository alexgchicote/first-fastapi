"""add content column to post table

Revision ID: 3cebc9ef768c
Revises: fcfbd9718c06
Create Date: 2022-01-31 12:27:46.479389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cebc9ef768c'
down_revision = 'fcfbd9718c06'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
