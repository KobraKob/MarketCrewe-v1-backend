# backend/main.py

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes.generate import generate_router
from routes.deliver_email import email_router
from routes.deliver_zip import zip_router
from routes.auth import auth_router, get_current_user # Import the new auth router and dependency

app = FastAPI(title="MarketCrew Delivery API")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Location"],  # Expose Location header for redirects
)

# Routes
app.include_router(generate_router, prefix="/generate", dependencies=[Depends(get_current_user)]) # Protect generate route
print("Generate router protected by get_current_user")
app.include_router(email_router, prefix="/deliver", dependencies=[Depends(get_current_user)]) # Protect deliver routes
print("Email router protected by get_current_user")
app.include_router(zip_router, prefix="/deliver", dependencies=[Depends(get_current_user)]) # Protect deliver routes
print("Zip router protected by get_current_user")
app.include_router(auth_router, prefix="/auth") # Include the new auth router
app.include_router(generate_router)
