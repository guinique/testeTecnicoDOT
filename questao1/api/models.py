from sqlalchemy import Column, Integer, String, Date, Text
from database import Base

# modelo do livro para o SQLAlchemy
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    public_date = Column(Date)
    summary = Column(Text, nullable=True)