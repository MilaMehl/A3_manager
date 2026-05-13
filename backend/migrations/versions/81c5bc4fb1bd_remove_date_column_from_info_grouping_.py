"""remove date column from info_grouping_requests

Revision ID: 81c5bc4fb1bd
Revises: 37d4ed2b712b
Create Date: 2026-04-22 09:00:06.917945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81c5bc4fb1bd'
down_revision = '37d4ed2b712b'
branch_labels = None
depends_on = None


def upgrade():
    # A coluna pode já ter sido removida diretamente no banco.
    # Usa batch_alter_table apenas se a coluna ainda existir.
    conn = op.get_bind()
    columns = [row[1] for row in conn.execute(sa.text("PRAGMA table_info(info_grouping_requests)"))]
    if 'date' in columns:
        with op.batch_alter_table('info_grouping_requests') as batch_op:
            batch_op.drop_column('date')


def downgrade():
    with op.batch_alter_table('info_grouping_requests') as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))
