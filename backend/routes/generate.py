from fastapi import APIRouter, HTTPException, Depends
from workflows.weekly_content_workflow import run_weekly_content_plan
from pydantic import BaseModel
from openai import RateLimitError
from routes.auth import get_current_user, UserProfile
from .auth import supabase

generate_router = APIRouter()

class ContentRequest(BaseModel):
    brand_name: str
    industry: str
    audience: str
    tone: str
    goals: str
    products: list[str]

@generate_router.post("/generate")
def generate_content(request: ContentRequest, current_user: UserProfile = Depends(get_current_user)):
    update_data = {
        "brand_name": request.brand_name,
        "industry": request.industry,
        "audience": request.audience,
        "tone": request.tone,
        "goals": ", ".join([goal.strip() for goal in request.goals.split(',')]),
        "products": request.products,
    }

    try:
        supabase.table("user_profiles").update(update_data).eq("id", current_user.id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user profile: {e}")

    context = {
        "brand_name": request.brand_name,
        "industry": request.industry,
        "audience": request.audience,
        "tone": request.tone,
        "goals": [goal.strip() for goal in request.goals.split(',')],
        "products": request.products
    }

    try:
        generated_content = run_weekly_content_plan(context)
        return {"content": generated_content}
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded. Please try again later. Details: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
