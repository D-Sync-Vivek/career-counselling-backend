import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from core.database import get_db
from core.security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from models.users import User, Profile, Mentor, UserRole
from schemas.user import UserCreate, UserResponse, Token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """ Register a new user and automatically generate their linked profile. """
    logger.info(f"Attempting to register new user: {user_data.email}")
    
    # 1. Check if user already exists
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # 2. Create the core User (Auth Data)
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_pw,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Get the newly generated UUID
    
    # 3. Create the linked Profile (Display Data)
    new_profile = Profile(
        user_id=new_user.id,
        full_name=user_data.full_name
    )
    db.add(new_profile)

    # 4. If they registered as a Mentor, create a blank Mentor row too
    if user_data.role == UserRole.mentor:
        new_mentor = Mentor(
            user_id=new_user.id,
            is_verified=False
        )
        db.add(new_mentor)

    db.commit()
    
    logger.info(f"User {new_user.email} successfully registered with Profile.")
    return new_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Log in to get a JWT Access Token. """
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # We now embed the User's UUID directly into the token for fast queries later!
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value, "user_id": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}