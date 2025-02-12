from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db.user import create_user, get_user_by_username
from app.models.user import User
from app.models.token import Token
from app.utils.bcrypt import get_password_hash, verify_password
from app.utils.jsonwebtoken import create_access_token, decode_token

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_token(token)
    if token_data is None:
        raise credentials_exception
    user_db: User = await get_user_by_username(token_data.username)
    user = User(**user_db)
    if not user:
        raise credentials_exception
    return user.username

async def authenticate_user(username: str, password: str):
    user_db = await get_user_by_username(username)
    user = User(**user_db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return True

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register")
async def register(user: User):
    user_exists = await get_user_by_username(user.username)
    if user_exists:
        raise HTTPException(400, "User already exists")
    hashed_password = get_password_hash(user.password)
    user_data = User(username=user.username, password=hashed_password)
    user_db = await create_user(user_data.model_dump())
    new_user = User(**user_db)
    access_token = create_access_token(data={"sub": new_user.username})
    return Token(access_token=access_token, token_type="bearer")