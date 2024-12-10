import datetime
from fastapi import APIRouter, HTTPException, Depends, Response
from app.models.user import User, LoginRequest, UserinDB
from app.utils.security import hash_password, verify_password, create_access_token, get_current_user
from app.crud.user import create_user, get_user_by_email, get_user_by_id
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
async def login(request: LoginRequest, response: Response):
    """Login endpoint to authenticate a user."""
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
        data={"sub": user["id"]},  # The "sub" is the user ID
        expires_delta=timedelta(hours=1)  # Token expiration time
    )

    # Set the JWT token in the response cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Prevent client-side JS access
        secure=True,  # Ensure it's only sent over HTTPS
    )

    return {"msg": "Login Successful", "token_type": "bearer"}


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Endpoint to get the current user's profile information."""
    user_id = current_user["user_id"]
    print(user_id)

    # Fetch the user from the database using user_id
    user = await get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"email": user["email"]}