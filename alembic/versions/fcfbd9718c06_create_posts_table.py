"""create posts table

Revision ID: fcfbd9718c06
Revises: 
Create Date: 2022-01-31 12:16:35.469497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcfbd9718c06'
down_revision = None
branch_labels = None
depends_on = None



# runs the commands for making 
# the changes that you want to do

# handles changes
def upgrade():
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False)
    )
    pass

# handles rollbacks 
def downgrade():
    op.drop_table('posts')
    pass
