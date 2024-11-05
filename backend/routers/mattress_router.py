from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db  
from schemas.schema import MattressOut 
from services.product_services import MattressService  

# Initialize the router
router = APIRouter(tags=["Mattresses"], prefix="/mattresses")

# Get all mattresses with optional filters
@router.get("/", response_model=List[MattressOut])
def get_mattresses(
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
    limit: int = 10,
    db: Session = Depends(get_db)
):
    mattresses = MattressService.filter_mattresses(
        db=db,
        name=name,
        size=size,
        current_price=current_price,
        rating=rating,
        num_reviews=num_reviews,
        comfort=comfort,
        best_for=best_for,
        mattress_type=mattress_type,
        height=height,
        cooling_technology=cooling_technology,
        motion_separation=motion_separation,
        pressure_relief=pressure_relief,
        support=support,
        adjustable_base_friendly=adjustable_base_friendly,
        breathable=breathable,
        mattress_in_a_box=mattress_in_a_box,
        skip=skip,
        limit=limit
    )
    
    if not mattresses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No mattresses found")

    return mattresses
