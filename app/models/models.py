from service.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class User(Base):
    __tablename__ = "USERTABLE"
    id = Column(Integer, primary_key= True, autoincrement= True)
    username = Column(String, unique= True, index= True)
    hashed_password = Column(String)

    CART_ITEMS = relationship("CartItem", back_populates="onwer")
    PURCHASE = relationship("Purchase", back_populates="buyer")

class Product(Base):
    __tablename__ = "PRODUCTSTABLE"
    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String, unique= True, index= True)
    description = Column(String, index= True)
    price = Column(Integer)
    stock = Column(Integer)

class CartItem(Base):
    __tablename__ = "CART_ITEMS"
    id = Column(Integer, primary_key= True, autoincrement= True)
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey('USERTABLE.id'))
    product_id = Column(Integer, ForeignKey('PRODUCTSTABLE.id'))


    onwer = relationship("User", back_populates="CART_ITEMS")
    product = relationship("Product")
    
class Purchase(Base):
    __tablename__ = "PURCHASE"
    id = Column(Integer, primary_key= True, autoincrement= True)
    total_price = Column(Float)
    user_id = Column(Integer, ForeignKey('USERTABLE.id'))

    product_id = Column(Integer, ForeignKey("PRODUCTSTABLE.id"))

    buyer = relationship("User", back_populates="PURCHASE")
    product = relationship("Product")