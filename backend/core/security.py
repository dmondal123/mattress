from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Configurations
SECRET_KEY = "my_secret_key"  # Replace with your own secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Decode and verify JWT token
def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")  # Debugging statement
        username: str = payload.get("sub")
        if username is None:
            raise JWTError("Token doesn't contain username.")
        return username
    except JWTError:
        print("Invalid token or decoding error.")  # Debugging statement
        return None

