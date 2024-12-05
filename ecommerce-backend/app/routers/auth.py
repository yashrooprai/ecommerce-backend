from fastapi import APIRouter, HTTPException
from app.models.user import User, LoginRequest, UserinDB
from app.utils.security import hash_password, verify_password, create_access_token
from app.crud.user import create_user, get_user_by_email
from datetime import timedelta

router = APIRouter()

@router.post("/signup")
async def signup(user: User):
    """Signup endpoint to create a new user."""
    # Check if the user already exists
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password before saving it
    hashed_password = hash_password(user.password)
    
    # Create a UserInDB object with hashed_password
    user_in_db = UserinDB(
        email=user.email,
        hashed_password=hashed_password,
    )
    
    # Create the user in the database
    user_data = await create_user(user_in_db)
    
    return {"msg": "User created successfully", "user": user_data}
@router.post("/login")
async def login(request: LoginRequest):
    """Login endpoint to authenticate a user."""
    # Extract email and password from the request body
    email = request.email
    password = request.password
    
    # Check if the user exists
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify the password
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(
        data={"sub": user["id"]},  # User's unique ID in the JWT payload
        expires_delta=timedelta(hours=1)  # Token expiration time
    )
    
    return {"access_token": access_token, "token_type": "bearer"}