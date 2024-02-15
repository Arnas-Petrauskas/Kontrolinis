from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///finansai.db')
Base = declarative_base()

class Finance(Base):
    __tablename__ = 'Finansai'
    id = Column(Integer, primary_key=True)
    type = Column("type", String) #Gali būti tik Income arba Expences
    amount = Column("amount", Integer) #Tik suma TIKRINTI INT
    category = Column("category", String) #Gali būti bet kas
    
    def __init__(self, type,amount,category):
        self.type = type
        self.amount = amount
        self.category = category

    
    def __repr__(self):
        return f"{self.id}, {self.type}, {self.amount},{self.category}"

Base.metadata.create_all(engine)