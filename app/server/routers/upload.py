from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from app.server.db_utils.cloud_manager import upload_file_implementation

router = APIRouter(
    tags=["upload"],
    prefix='/upload',
    responses={404: {"description": "Not found"}},
)


class UploadParams(BaseModel):
    pass


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
