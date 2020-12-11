"""First revision

Revision ID: d4867f3a4c0a
Revises:
Create Date: 2019-04-17 13:53:32.978401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d4867f3a4c0a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.dialects.postgresql.UUID(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("bio", sa.String(), nullable=True),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("social_urls", sa.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_name"), "user", ["name"], unique=False)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "lectureType",
        sa.Column("id", sa.Integer(), nullable=True,),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "lecture",
        sa.Column("id", sa.dialects.postgresql.UUID(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("author_id", sa.dialects.postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["user.id"],),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["type_id"], ["lectureType.id"],),
        sa.Column("thumbnail_url", sa.String(), nullable=True),
        sa.Column("excerpt", sa.String(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False),
        sa.Column("pdf_download_url", sa.String(), nullable=True),
        sa.Column("slug", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_lecture_title"), "lecture", ["title"], unique=False)
    op.create_index(op.f("ix_author_id"), "lecture", ["id"], unique=False)
    op.create_index(op.f("ix_lecture_id"), "lecture", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_lecture_title"), table_name="lecture")
    op.drop_index(op.f("ix_lecture_id"), table_name="lecture")
    op.drop_index(op.f("ix_author_id"), table_name="lecture")
    op.drop_table("lecture")
    op.drop_table("lectureType")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_name"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
