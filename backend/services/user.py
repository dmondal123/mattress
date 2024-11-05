# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from datetime import datetime, timedelta

# # Configuration
# SECRET_KEY = "my_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Hash password
# def get_password_hash(password: str):
#     return pwd_context.hash(password)

# # Verify password
# def verify_password(plain_password: str, hashed_password: str):
#     return pwd_context.verify(plain_password, hashed_password)

# # Create JWT token
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Decode and verify JWT token
# def decode_access_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise JWTError()
#         return username
#     except JWTError:
#         return None


# from sqlalchemy.orm import Session
# from models.models import User
# from schemas.user import UserCreate
# from core.security import get_password_hash

# class UserService:

#     @staticmethod
#     def create_user(db: Session, user: UserCreate):
#         hashed_password = get_password_hash(user.password)
#         db_user = User(
#             username=user.username,
#             email=user.email,
#             full_name=user.full_name,
#             hashed_password=hashed_password
#         )
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user

#     @staticmethod
#     def get_user_by_username(db: Session, username: str):
#         return db.query(User).filter(User.username == username).first()

#     @staticmethod
#     def get_current_user_from_token(token: str, db: Session):
#         # This will call the security function to decode the token
#         from core.security import decode_access_token
#         username = decode_access_token(token)
#         if username:
#             return UserService.get_user_by_username(db, username)
#         return None

from sqlalchemy.orm import Session
from models.models import User
from schemas.user import UserCreate
from core.security import get_password_hash, decode_access_token

class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_current_user_from_token(token: str, db: Session):
        # Decode the token to get the username
        username = decode_access_token(token)
        if username:
            # Query the user using the username (a string)
            return UserService.get_user_by_username(db, username)
        return None
