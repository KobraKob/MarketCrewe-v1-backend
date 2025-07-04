import os
from fastapi import APIRouter, HTTPException, Depends, status, Request
from pydantic import BaseModel
from supabase import create_client, Client
from datetime import datetime, timezone
from dotenv import load_dotenv
from typing import Optional

load_dotenv(dotenv_path='../.env')

auth_router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"Supabase URL: {SUPABASE_URL}")
print(f"Supabase Key (first 5 chars): {SUPABASE_KEY[:5] if SUPABASE_KEY else None}")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in the .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class UserCredentials(BaseModel):
    email: str
    password: str

class UserFormData(BaseModel):
    brand_name: str = ""
    industry: str = ""
    audience: str = ""
    tone: str = "friendly"
    goals: str = ""
    products: list[str] = []

class UserProfile(BaseModel):
    id: str
    brand_name: str
    industry: str
    audience: str
    tone: str
    goals: str
    products: list
    email: Optional[str] = None

    class Config:
        extra = 'ignore'

async def get_current_user(request: Request) -> UserProfile:
    auth_header = request.headers.get("Authorization")
    print(f"Authorization Header: {auth_header}")

    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    token_parts = auth_header.split(" ")
    if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format")

    token = token_parts[1]
    print(f"Extracted Token: {token[:10]}...")  # First 10 chars

    try:
        user_response = supabase.auth.get_user(token)
        print(f"User Response from Supabase: {user_response}")
        if not user_response or not user_response.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

        user_id = user_response.user.id
        user_email = user_response.user.email

        response = supabase.table("user_profiles").select("*").eq("id", user_id).execute()
        print(f"User profile query response data: {response.data}")

        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

        user_profile_data = response.data[0]



        return UserProfile(**user_profile_data)
    except Exception as e:
        print(f"Error during token validation: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token validation failed: {e}")

@auth_router.post("/register")
async def register_user(user: UserCredentials):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })

        if response.user:
            user_id = response.user.id
            user_email = response.user.email

            # Create a default user profile matching the database schema
            default_profile = {
                "id": user_id,
                "brand_name": "",
                "industry": "",
                "audience": "",
                "tone": "friendly",
                "goals": "",
                "products": [],
                "email": user_email,
            }

            # Insert the default profile into the user_profiles table
            supabase.table("user_profiles").insert(default_profile).execute()

            return {"message": "User registered successfully", "user": response.user.email, "user_profile": default_profile}
        else:
            raise HTTPException(status_code=400, detail=response.session.user.identities)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/login")
async def login_user(user: UserCredentials):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })

        if not response.user:
            raise HTTPException(status_code=400, detail="Authentication failed")

        user_id = response.user.id
        user_email = response.user.email

        profile_response = supabase.table("user_profiles").select("*").eq("id", user_id).single().execute()

        if not profile_response.data:
            default_profile = {
                "id": user_id,
                "email": user_email,
                "brand_name": "",
                "industry": "",
                "audience": "",
                "tone": "friendly",
                "goals": "",
                "products": []
            }
            supabase.table("user_profiles").insert(default_profile).execute()
            user_profile = UserProfile(**default_profile)
        else:
            user_profile = UserProfile(**profile_response.data)

        return {
            "message": "User logged in successfully",
            "user": user_email,
            "token": response.session.access_token,
            "user_profile": user_profile.dict()
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")

@auth_router.get("/me", response_model=UserProfile)
async def read_users_me(current_user: UserProfile = Depends(get_current_user)):
    return current_user
