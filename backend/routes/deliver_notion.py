# backend/routes/deliver_notion.py

from fastapi import APIRouter

notion_router = APIRouter()  # This must exist!

@notion_router.post("/notion")
def push_to_notion():
    return {"status": "info", "message": "Notion integration is currently disabled."}