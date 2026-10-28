"""baseline

Revision ID: 0001
Revises:
Create Date: 2026-10-28

Empty baseline: establishes the migration chain. Tables arrive with the tickets
that need them (#6 users/accounts/ledger, #8 games, ...).
"""

from collections.abc import Sequence

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
