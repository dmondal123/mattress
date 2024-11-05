from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user import UserCreate, UserLogin, Token, UserOut
from services.user import UserService
from core.security import create_access_token, verify_password
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from fastapi import Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse



router = APIRouter(tags=["Auth"], prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 30




# User Registration
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = UserService.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return UserService.create_user(db, user)


# User Login
# @router.post("/login", response_model=Token)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = UserService.get_user_by_username(db, user.username)
#     if not db_user or not verify_password(user.password, db_user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password"
#         )

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": db_user.username},
#         expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_username(db, user.username)
    

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )
    
    
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,  
        secure=True,  
        samesite="Lax", 
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  
    )
    
   
    return {"token": access_token}


# Get the current logged-in user
@router.get("/me", response_model=UserOut)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = UserService.get_current_user_from_token(token, db)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return UserService.get_user_by_username(db, username)
