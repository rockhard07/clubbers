from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Optional
import os

from config.supabase import supabase
from app.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="Clubbers API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # Query user from Supabase
    response = supabase.table('users').select('*').eq('email', form_data.username).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = response.data[0]
    if not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
async def register(
    email: str,
    username: str,
    password: str,
    full_name: str,
):
    # Check if user already exists
    response = supabase.table('users').select('*').eq('email', email).execute()
    if response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(password)
    user_data = {
        'email': email,
        'username': username,
        'hashed_password': hashed_password,
        'full_name': full_name
    }
    
    response = supabase.table('users').insert(user_data).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    return {"message": "User created successfully"}

@app.get("/users/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme)
):
    # In a real application, you would decode the token and get the user
    # For now, we'll just return a mock response
    return {"message": "User profile endpoint"}

@app.post("/upload-profile-image")
async def upload_profile_image(
    image: bytes,
    token: str = Depends(oauth2_scheme)
):
    # TODO: Implement image upload to Supabase Storage
    return {"message": "Image upload endpoint"} 