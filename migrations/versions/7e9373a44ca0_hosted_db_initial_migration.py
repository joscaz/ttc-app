"""Hosted db initial migration

Revision ID: 7e9373a44ca0
Revises: 
Create Date: 2024-06-08 01:45:36.857951

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7e9373a44ca0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('codigo',
    sa.Column('id_codigo', sa.Integer(), nullable=False),
    sa.Column('nombre_archivo', sa.String(length=100), nullable=False),
    sa.Column('contenido', sa.Text(), nullable=False),
    sa.Column('fecha_subida', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id_codigo')
    )
    op.create_table('elemento',
    sa.Column('id_elemento', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('localizador', sa.String(length=200), nullable=False),
    sa.Column('estado', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id_elemento')
    )
    op.create_table('version',
    sa.Column('id_version', sa.Integer(), nullable=False),
    sa.Column('numero_version', sa.String(length=50), nullable=False),
    sa.Column('github_url', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id_version')
    )
    op.create_table('prueba',
    sa.Column('id_prueba', sa.Integer(), nullable=False),
    sa.Column('nombre_prueba', sa.String(length=100), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('estado', sa.Boolean(), nullable=False),
    sa.Column('cambio_aceptado', sa.Boolean(), nullable=False),
    sa.Column('id_codigo', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_codigo'], ['codigo.id_codigo'], ),
    sa.PrimaryKeyConstraint('id_prueba')
    )
    op.create_table('reporte',
    sa.Column('id_reporte', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('contenido', sa.Text(), nullable=False),
    sa.Column('id_pruebas', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('id_codigo', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_codigo'], ['codigo.id_codigo'], ),
    sa.PrimaryKeyConstraint('id_reporte')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reporte')
    op.drop_table('prueba')
    op.drop_table('version')
    op.drop_table('elemento')
    op.drop_table('codigo')
    # ### end Alembic commands ###