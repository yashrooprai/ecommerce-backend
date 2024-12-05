from app.database import db, to_dict
from app.models.user import UserinDB

async def create_user(user: UserinDB) -> dict:
    """Insert a new user into the database."""
    result = await db.users.insert_one(user.dict(exclude={"id"}))
    user.id = str(result.inserted_id)
    return user.dict()

async def get_user_by_email(email: str):
    """Find a user by their email."""
    user = await db.users.find_one({"email": email})
    if user:
        return to_dict(user)
    else:
        return None
    
