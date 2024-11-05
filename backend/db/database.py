# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from credentials import set_credentials
import os
set_credentials()



DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')  
DB_PORT = os.getenv('DB_PORT')  


# Replace with your Cloud SQL MySQL database URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Replace with your Cloud SQL MySQL database URL (for example)
# # For mysqlclient (recommended for production):
# # SQLALCHEMY_DATABASE_URL = "mysql://user:password@cloudsql_instance_ip/db_name"

# # For PyMySQL (pure Python, simpler installation):
# # SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@cloudsql_instance_ip/db_name"

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Rakesh123@localhost:3306/my_local_db"


# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Dependency to get the DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

