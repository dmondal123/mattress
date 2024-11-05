from pydantic import BaseModel, EmailStr

# Model for creating a new user
class UserCreate(BaseModel):
    username: str
    password: str  
    email: EmailStr  # Use EmailStr for email validation
    

# Model for user login
class UserLogin(BaseModel):
    username: str
    password: str

# Model for outputting user details
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr  # Use EmailStr for consistent email handling
    

    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy models

# Model for the token response
class Token(BaseModel):
    access_token: str
    token_type: str
