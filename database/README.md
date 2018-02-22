# Alembic migrations

To create a migration file: `alembic revision -m "Create Foo Table"`


To run migrations: `alembic upgrade head [--sql]`
--sql generates table statements without applying them to the database, this is useful for making sure your table is right before you apply it
