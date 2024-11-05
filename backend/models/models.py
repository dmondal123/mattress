from sqlalchemy import Column, Integer, String,Float, JSON, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # specify the length for VARCHAR
    email = Column(String(100), unique=True, index=True)     # also specify length here
    password = Column(String(100))                            # and here

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), index=True)                  # Length specified
#     description = Column(String(1000))                        # Specify length (e.g., 1000)
#     price = Column(Float, nullable=False)                     # Ensure price is required
#     discount_percentage = Column(Float, nullable=True)
#     dimensions = Column(String(50))                           # Length specified
#     comfort_type = Column(String(50))                         # Length specified
#     material = Column(String(50))                             # Length specified
#     brand = Column(String(100))                               # Length specified
#     stock = Column(Integer, default=0)                        # Default stock
#     thumbnail = Column(String(255))                           # Length specified
#     images = Column(String(1000))                             # Specify length (e.g., 1000)
#     is_published = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     category_id = Column(Integer, ForeignKey('categories.id'))

#     category = relationship("Category", back_populates="products")

# class Category(Base):
#     __tablename__ = "categories"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), unique=True)                   # Length specified

#     products = relationship("Product", back_populates="category")




class Mattress(Base):
    __tablename__ = 'mattresses'
    
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    size = Column(String(50))
    images = Column(JSON)               # Storing image paths in JSON format
    current_price = Column(DECIMAL(10, 2))
    rating = Column(Float)              # Using Float for ratings like 4.1
    num_reviews = Column(Integer)
    comfort = Column(String(50))
    best_for = Column(String(100))
    mattress_type = Column(String(100))
    height = Column(String(10))         # Storing height as string to handle units
    cooling_technology = Column(String(50))
    motion_separation = Column(String(10))
    pressure_relief = Column(String(10))
    support = Column(String(10))
    adjustable_base_friendly = Column(String(10))
    breathable = Column(String(10))
    mattress_in_a_box = Column(String(10))
