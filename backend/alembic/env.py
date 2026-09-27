from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.models.base import Base
from app.core.config import settings

from app.models import *
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# A caller that already set this (the Postgres test suite's per-test schema
# fixture, tests/postgres/conftest.py, passing its own Config instance to
# alembic.command.*) is respected rather than clobbered here -- every real
# invocation (CLI, the compose `migrate` service) never pre-sets it, so this
# is unchanged for them. alembic.ini's own `sqlalchemy.url =` is blank, so
# `or` falls through to Settings() exactly as before when nothing did.
config.set_main_option(
    "sqlalchemy.url",
    config.get_main_option("sqlalchemy.url", "") or settings.DATABASE_URL,
)
# Interpret the config file for Python logging. disable_existing_loggers
# defaults to True, which -- when this module is exec'd programmatically
# mid-test-session rather than as a standalone CLI process -- silently
# disables every logger already configured (e.g. by conftest.py or by
# app modules imported earlier in the same process), breaking any later
# test that asserts on captured log output. False matches what a fresh CLI
# process already gets for free (there are no "existing" loggers to keep).
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    """Exclude `corpus_documents.search_vector` from autogenerate.

    It is a generated Postgres `tsvector` column created by raw SQL in its
    migration (ADR-007 decision 2), never declared on the `CorpusDocument`
    ORM model, so that SQLite -- the fast test suite's engine -- never has
    to represent a type it does not support. Without this hook, autogenerate
    would see it in the reflected database but not in `target_metadata` and
    propose dropping it on every run.
    """

    if type_ == "column" and name == "search_vector" and object.table.name == "corpus_documents":
        return False
    return True

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # print("Alembic URL:", config.get_main_option("sqlalchemy.url"))
    # print("Section:", config.get_section(config.config_ini_section))
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
