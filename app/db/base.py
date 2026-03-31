from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# IMPORTANT: import models so Alembic can discover them
# from app.models.user import User  # noqa: F401
# from app.models.application import Application  # noqa: F401