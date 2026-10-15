"""create resources table

Revision ID: 0001
Revises:
Create Date: 2026-10-15
"""

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "resources",  # Nueva tabla
        sa.Column("id", sa.Integer(), nullable=False),  # ID obligatorio
        sa.Column("name", sa.String(length=100), nullable=False),  # Nombre requerido
        sa.Column("type", sa.String(length=50), nullable=False),  # Tipo de recurso
        sa.Column("status", sa.String(length=30), nullable=False),  # Estado actual
        sa.Column("location", sa.String(length=150), nullable=True),  # Ubicación opcional
        sa.PrimaryKeyConstraint("id"),  # Clave primaria
    )


def downgrade() -> None:
    op.drop_table("resources")  # Revierte la migración
