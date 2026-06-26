from sqlalchemy import Column, Integer, String, Float
from database import Base


# Create the Base class (my database models will inherit from this)




class Product(Base):
    __tablename__ = "product "

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)  


#postgreSQL only understands tables, columns, and SQL text. Python only understands objects, classes, and attributes. Base is the translator machine that maps your Python class rules directly into PostgreSQL database structures.Analogy: It is an official registration form. Any class that inherits from Base (like class DBProduct(Base)) gets automatically registered so SQLAlchemy knows exactly how to build that table in your database