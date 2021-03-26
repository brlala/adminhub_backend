import io
import mimetypes
import os
from datetime import datetime

import requests
from fastapi import APIRouter, File, UploadFile, HTTPException

from app.server.db_utils.cloud_manager import upload_file_implementation
from app.server.models.upload import UploadUrl
from app.server.utils.common import FileBytesIO

router = APIRouter(
    tags=["upload"],
    prefix='/upload',
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    url = await upload_file_implementation(file)
    result = {
        "url": url,
        "success": True,
    }
    return result


@router.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "type": file.content_type}


@router.post("/url/")
async def create_upload_file(upload: UploadUrl):
    res = requests.get(upload.url)
    dl_file = io.BytesIO(res.content)
    content_type = res.headers['Content-Type'].split(';')[0]
    if not content_type or not (content_type.startswith('image') or content_type.startswith('video')):
        res = {
            "url": upload.url,
            "status": False,
            "detail": "URL provided is invalid. Only 'image' and 'video' URL is currently supported."
        }
        raise HTTPException(status_code=400, detail=res)
    # _, filename = os.path.split(upload.url)
    extension = mimetypes.guess_extension(content_type)
    filename = f'urlupload_{datetime.now().strftime("%Y%m%d_%H%M%S")}{extension}'
    file = FileBytesIO(dl_file, filename=filename, content_type=content_type)
    url = await upload_file_implementation(file)
    result = {
        "url": url,
        "success": True,
    }
    return result
