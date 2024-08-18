from database import Base
from sqlalchemy import Column, Integer, String


class MyTable(Base):
    __tablename__ = "my_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    country_code = Column(String)
    balance = Column(Integer)
