from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.models import Mattress
from schemas.schema import MattressCreate
import json


class MattressService:

    @staticmethod
    def create_mattress(db: Session, mattress: MattressCreate):
        # Ensure images is saved as a list in the database
        db_mattress = Mattress(
            name=mattress.name,
            size=mattress.size,
            # Convert JSON string to list if necessary
            images=json.loads(mattress.images) if isinstance(mattress.images, str) else mattress.images,
            current_price=mattress.current_price,
            rating=mattress.rating,
            num_reviews=mattress.num_reviews,
            comfort=mattress.comfort,
            best_for=mattress.best_for,
            mattress_type=mattress.mattress_type,
            height=mattress.height,
            cooling_technology=mattress.cooling_technology,
            motion_separation=mattress.motion_separation,
            pressure_relief=mattress.pressure_relief,
            support=mattress.support,
            adjustable_base_friendly=mattress.adjustable_base_friendly,
            breathable=mattress.breathable,
            mattress_in_a_box=mattress.mattress_in_a_box,
        )
        db.add(db_mattress)
        db.commit()
        db.refresh(db_mattress)
        return db_mattress

    @staticmethod
    def filter_mattresses(
        db: Session,
        name: Optional[str] = None,
        size: Optional[str] = None,
        current_price: Optional[float] = None,
        rating: Optional[float] = None,
        num_reviews: Optional[int] = None,
        comfort: Optional[str] = None,
        best_for: Optional[str] = None,
        mattress_type: Optional[str] = None,
        height: Optional[str] = None,
        cooling_technology: Optional[str] = None,
        motion_separation: Optional[str] = None,
        pressure_relief: Optional[str] = None,
        support: Optional[str] = None,
        adjustable_base_friendly: Optional[str] = None,
        breathable: Optional[str] = None,
        mattress_in_a_box: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Mattress]:
        # Create a list of conditions based on the provided filters
        conditions = []
        if name:
            conditions.append(Mattress.name.ilike(f"%{name}%"))
        if size:
            conditions.append(Mattress.size == size)
        if current_price:
            conditions.append(Mattress.current_price == current_price)
        if rating:
            conditions.append(Mattress.rating == rating)
        if num_reviews:
            conditions.append(Mattress.num_reviews == num_reviews)
        if comfort:
            conditions.append(Mattress.comfort.ilike(f"%{comfort}%"))
        if best_for:
            conditions.append(Mattress.best_for.ilike(f"%{best_for}%"))
        if mattress_type:
            conditions.append(Mattress.mattress_type.ilike(f"%{mattress_type}%"))
        if height:
            conditions.append(Mattress.height == height)
        if cooling_technology:
            conditions.append(Mattress.cooling_technology.ilike(f"%{cooling_technology}%"))
        if motion_separation:
            conditions.append(Mattress.motion_separation == motion_separation)
        if pressure_relief:
            conditions.append(Mattress.pressure_relief == pressure_relief)
        if support:
            conditions.append(Mattress.support == support)
        if adjustable_base_friendly:
            conditions.append(Mattress.adjustable_base_friendly == adjustable_base_friendly)
        if breathable:
            conditions.append(Mattress.breathable == breathable)
        if mattress_in_a_box:
            conditions.append(Mattress.mattress_in_a_box == mattress_in_a_box)
        
        # Build and execute the query with the specified filters
        query = db.query(Mattress).filter(and_(*conditions)).offset(skip).limit(limit)
        results = query.all()
        
        # Ensure images are returned as lists, not JSON strings
        for result in results:
            if isinstance(result.images, str):
                try:
                    result.images = json.loads(result.images.replace('\\', '\\\\'))
                except json.JSONDecodeError as e:
                    # Log the error or handle it as needed
                    print(f"JSON decoding error for Mattress ID {result.id}: {e}")
                    result.images = []  # Fallback to an empty list if JSON parsing fails
        
        return results
