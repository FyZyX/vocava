## Database Migrations

1. Install Alembic: `pip install alembic`
2. Navigate to your project root directory and initiate Alembic: `alembic init alembic`
3. Configure Alembic: Open the `alembic.ini` file that was generated in your project root directory and change the `sqlalchemy.url` to the URI of your database.
4. Modify `env.py`: You'll need to provide the `Base` and `engine` from your SQLAlchemy models to Alembic's `env.py` file in the `alembic` directory.
5. Generate a migration: After you've made changes to your models, you can generate a migration script with `alembic revision --autogenerate -m "description of your changes"`. This will create a new script in the `alembic/versions` directory.
6. Apply migrations: You can upgrade your database to a later version with `alembic upgrade head` or downgrade to an earlier version with `alembic downgrade -1`.