"""empty message

Revision ID: c32087bda874
Revises: 
Create Date: 2019-07-16 20:12:58.552277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c32087bda874'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_name', sa.String(length=64), nullable=True),
    sa.Column('appointment_time', sa.DateTime(), nullable=True),
    sa.Column('advisor_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_name', 'appointment_time', name='_unique_student_and_time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointment')
    # ### end Alembic commands ###