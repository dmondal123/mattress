from pydantic import BaseModel, condecimal
from typing import Optional, List

# Model for creating a new mattress entry
class MattressCreate(BaseModel):
    name: str
    size: str
    images: Optional[List[str]] = []         # List of image URLs, optional field
    current_price: condecimal(max_digits=10, decimal_places=2)  # Exact currency format
    rating: Optional[float] = None           # Rating can be optional
    num_reviews: Optional[int] = None
    comfort: Optional[str] = None
    best_for: Optional[str] = None
    mattress_type: Optional[str] = None
    height: Optional[str] = None
    cooling_technology: Optional[str] = None
    motion_separation: Optional[str] = None
    pressure_relief: Optional[str] = None
    support: Optional[str] = None
    adjustable_base_friendly: Optional[str] = None
    breathable: Optional[str] = None
    mattress_in_a_box: Optional[str] = None

# Model for outputting mattress details
class MattressOut(BaseModel):
    product_id: int
    name: str
    size: str
    images: List[str]
    current_price: condecimal(max_digits=10, decimal_places=2)
    rating: Optional[float]
    num_reviews: Optional[int]
    comfort: Optional[str]
    best_for: Optional[str]
    mattress_type: Optional[str]
    height: Optional[str]
    cooling_technology: Optional[str]
    motion_separation: Optional[str]
    pressure_relief: Optional[str]
    support: Optional[str]
    adjustable_base_friendly: Optional[str]
    breathable: Optional[str]
    mattress_in_a_box: Optional[str]

    class Config:
        from_attributes = True  # Ensures compatibility with SQLAlchemy model attributes
