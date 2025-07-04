# backend/routes/deliver_zip.py

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import os

zip_router = APIRouter()

class DownloadRequest(BaseModel):
    brand_name: str

@zip_router.post("/download")
def download_content(request: DownloadRequest):
    zip_path = "delivery/content_bundle.zip"

    # Remove old zip if exists
    if os.path.exists(zip_path):
        os.remove(zip_path)

    shutil.make_archive("delivery/content_bundle", 'zip', "delivery/")
    return FileResponse(path=zip_path, filename=f"{request.brand_name.replace(' ', '_')}_marketcrew.zip", media_type='application/zip')
