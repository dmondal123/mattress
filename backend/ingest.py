import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Mattress  # SQLAlchemy model for the mattresses table
from db.database import Base
import os   # Base class for SQLAlchemy

# Define your database connection URI - replace with correct details

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')  
DB_PORT = os.getenv('DB_PORT')  


# Replace with your Cloud SQL MySQL database URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DATABASE_URI = "mysql+pymysql://username:password@127.0.0.1:3306/your_database"

# Create SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the mattresses table in the database if it doesn't exist
Base.metadata.create_all(bind=engine)

# Load the CSV data, assuming the first row is column names
file_path = '/Users/rakkumar/Downloads/Final_CSV_Data_with_Differentiated_Product_IDs.csv'
data = pd.read_csv(file_path)

# Function to insert data into the database
def ingest_data(session, data):
    try:
        # Iterate through each row and create a Mattress instance
        for _, row in data.iterrows():
            mattress = Mattress(
                product_id=row['product_id'],
                name=row['name'],
                size=row['size'],
                images=row['images'],  # Assuming JSON format in CSV
                current_price=row['current_price'],
                rating=row['rating'],
                num_reviews=row['num_reviews'],
                comfort=row['comfort'],
                best_for=row['best_for'],
                mattress_type=row['mattress_type'],
                height=row['height'],
                cooling_technology=row['cooling_technology'],
                motion_separation=row['motion_separation'],
                pressure_relief=row['pressure_relief'],
                support=row['support'],
                adjustable_base_friendly=row['adjustable_base_friendly'],
                breathable=row['breathable'],
                mattress_in_a_box=row['mattress_in_a_box']
            )
            session.add(mattress)
        
        # Commit the transaction in batches for efficiency
        session.commit()
    except Exception as e:
        print("Error occurred:", e)
        session.rollback()
    finally:
        session.close()

# Main execution
if __name__ == "__main__":
    # Start a session and ingest data
    with SessionLocal() as session:
        ingest_data(session, data)
