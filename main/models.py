from sqlalchemy import (
    Column,
    Integer,
    create_engine,
    String,
    Date,
)

from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///tasks_db.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)

    def __repr__(self):
        return f"{self.title}, {self.description}, {self.status}, {self.created_at}, {self.updated_at}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
