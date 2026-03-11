from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

# This class = one table in PostgreSQL called "tasks"
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)       # Auto ID
    title = Column(String, nullable=False)                    # Task name
    description = Column(String, nullable=True)               # Optional detail
    completed = Column(Boolean, default=False)                # Done or not?