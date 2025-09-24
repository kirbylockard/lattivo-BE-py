# pylint: skip-file
# # ruff: noqa: I001
# tell ruff to ignore the unused import error for this file
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.core.database import Base, DATABASE_URL

# Convert async URL to sync for Alembic
sync_database_url = DATABASE_URL.replace("+asyncpg", "")

config = context.config
config.set_main_option("sqlalchemy.url", sync_database_url)
# tell ruff to ignore "import not at top of file" and "unused import" below
from app.models import habit  # noqa: E402, F401
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
