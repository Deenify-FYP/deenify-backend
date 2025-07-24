from fastapi import APIRouter,UploadFile,File,Form,Request,HTTPException
from app.services.recitation import process_recitation

router = APIRouter()

@router.post("/recite")
async def recite(
    request: Request,
    audio: UploadFile = File(...),
    surah_number: int = Form(...),
    ayah_number: int = Form(...)
):
    if not audio.content_type.startswith("audio/"):
        raise HTTPException(status_code=400,detail="Not a valid audio file!")
    return await process_recitation(request,audio,surah_number,ayah_number)