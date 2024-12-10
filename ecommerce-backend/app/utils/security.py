from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "700007"  # Replace with a secure random key
ALGORITHM = "HS256"  # Hashing algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(request: Request) -> dict:
    """Get the current user by verifying the JWT token from cookies."""
    token = request.cookies.get("access_token")  # Extract token from cookies
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    """Generate a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict:
    """Validate and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
