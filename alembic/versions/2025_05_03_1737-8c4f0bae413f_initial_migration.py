"""Initial migration

Revision ID: 8c4f0bae413f
Revises: 
Create Date: 2025-05-03 17:37:33.383146

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8c4f0bae413f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("name", name=op.f("uq_categories_name")),
    )
    op.create_table(
        "reactions",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reactions")),
        sa.UniqueConstraint("name", name=op.f("uq_reactions_name")),
    )
    op.create_table(
        "tags",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tags")),
        sa.UniqueConstraint("name", name=op.f("uq_tags_name")),
    )
    op.create_table(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "posts",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("body", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("draft", "published", "archived", name="statuses"),
            nullable=False,
        ),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column(
            "post_views",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
            name=op.f("fk_posts_author_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_posts")),
        sa.UniqueConstraint("title", name="unique_post"),
    )
    op.create_index(
        op.f("ix_posts_author_id"), "posts", ["author_id"], unique=False
    )
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("reply_to", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
            name=op.f("fk_comments_post_id_posts"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["reply_to"],
            ["comments.id"],
            name=op.f("fk_comments_reply_to_comments"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_comments_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_comments")),
    )
    op.create_index(op.f("ix_comments_id"), "comments", ["id"], unique=False)
    op.create_index(
        op.f("ix_comments_post_id"), "comments", ["post_id"], unique=False
    )
    op.create_index(
        op.f("ix_comments_reply_to"), "comments", ["reply_to"], unique=False
    )
    op.create_index(
        op.f("ix_comments_user_id"), "comments", ["user_id"], unique=False
    )
    op.create_table(
        "posts_categories",
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_posts_categories_category_id_categories"),
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
            name=op.f("fk_posts_categories_post_id_posts"),
        ),
        sa.UniqueConstraint("post_id", "category_id", name="uq_post_category"),
    )
    op.create_index(
        op.f("ix_posts_categories_category_id"),
        "posts_categories",
        ["category_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_posts_categories_post_id"),
        "posts_categories",
        ["post_id"],
        unique=False,
    )
    op.create_table(
        "posts_tags",
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column("tag_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["post_id"], ["posts.id"], name=op.f("fk_posts_tags_post_id_posts")
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tags.id"], name=op.f("fk_posts_tags_tag_id_tags")
        ),
        sa.UniqueConstraint("post_id", "tag_id", name="uq_post_tag"),
    )
    op.create_index(
        op.f("ix_posts_tags_post_id"), "posts_tags", ["post_id"], unique=False
    )
    op.create_index(
        op.f("ix_posts_tags_tag_id"), "posts_tags", ["tag_id"], unique=False
    )
    op.create_table(
        "user_post_votes",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column(
            "vote_type",
            sa.Enum("like", "dislike", name="votestatuses"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
            name=op.f("fk_user_post_votes_post_id_posts"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_post_votes_user_id_users"),
        ),
        sa.UniqueConstraint("user_id", "post_id", name="uq_user_post"),
    )
    op.create_index(
        op.f("ix_user_post_votes_post_id"),
        "user_post_votes",
        ["post_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_post_votes_user_id"),
        "user_post_votes",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "users_comments_reactions",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("comment_id", sa.Integer(), nullable=True),
        sa.Column("reaction_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["comment_id"],
            ["comments.id"],
            name=op.f("fk_users_comments_reactions_comment_id_comments"),
        ),
        sa.ForeignKeyConstraint(
            ["reaction_id"],
            ["reactions.id"],
            name=op.f("fk_users_comments_reactions_reaction_id_reactions"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_users_comments_reactions_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_users_comments_reactions")
        ),
        sa.UniqueConstraint(
            "user_id",
            "comment_id",
            "reaction_id",
            name="uq_users_comments_reactions",
        ),
    )
    op.create_index(
        op.f("ix_users_comments_reactions_comment_id"),
        "users_comments_reactions",
        ["comment_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_users_comments_reactions_reaction_id"),
        "users_comments_reactions",
        ["reaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_users_comments_reactions_user_id"),
        "users_comments_reactions",
        ["user_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_users_comments_reactions_user_id"),
        table_name="users_comments_reactions",
    )
    op.drop_index(
        op.f("ix_users_comments_reactions_reaction_id"),
        table_name="users_comments_reactions",
    )
    op.drop_index(
        op.f("ix_users_comments_reactions_comment_id"),
        table_name="users_comments_reactions",
    )
    op.drop_table("users_comments_reactions")
    op.drop_index(
        op.f("ix_user_post_votes_user_id"), table_name="user_post_votes"
    )
    op.drop_index(
        op.f("ix_user_post_votes_post_id"), table_name="user_post_votes"
    )
    op.drop_table("user_post_votes")
    op.drop_index(op.f("ix_posts_tags_tag_id"), table_name="posts_tags")
    op.drop_index(op.f("ix_posts_tags_post_id"), table_name="posts_tags")
    op.drop_table("posts_tags")
    op.drop_index(
        op.f("ix_posts_categories_post_id"), table_name="posts_categories"
    )
    op.drop_index(
        op.f("ix_posts_categories_category_id"), table_name="posts_categories"
    )
    op.drop_table("posts_categories")
    op.drop_index(op.f("ix_comments_user_id"), table_name="comments")
    op.drop_index(op.f("ix_comments_reply_to"), table_name="comments")
    op.drop_index(op.f("ix_comments_post_id"), table_name="comments")
    op.drop_index(op.f("ix_comments_id"), table_name="comments")
    op.drop_table("comments")
    op.drop_index(op.f("ix_posts_author_id"), table_name="posts")
    op.drop_table("posts")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("tags")
    op.drop_table("reactions")
    op.drop_table("categories")
    # ### end Alembic commands ###
