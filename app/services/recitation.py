from typing import TypedDict
from fastapi import UploadFile,Request
from app.utils.fetch_ayah_data import fetch_ayah_data
from app.utils.transcribe_audio import transcribe_audio

class AyahTypesenseSchema(TypedDict):
    id: int
    text: str
    ayah_number: int
    surah_number: int
    surah_name_en: str

async def process_recitation(request:Request,audio: UploadFile, surah_number: int, ayah_number: int):

    #Fetching the real API Ayah here
    api_url = "http://api.alquran.cloud/v1/ayah/"
    data = await fetch_ayah_data(ayah_number,surah_number,api_url)

    #Parsing the real Ayah data
    ayah_data = data["data"]
    ayah_document: AyahTypesenseSchema = {
        "id": ayah_data["number"],
        "text": ayah_data["text"],
        "ayah_number": ayah_data["numberInSurah"],
        "surah_number": ayah_data["surah"]["number"],
        "surah_name_en": ayah_data["surah"]["englishName"]
    }
    splitted_ayah = [word.strip() for word in ayah_document["text"].split(" ")]

    #Converting user's audio recitation to text
    audio_to_text = await transcribe_audio(request,audio)
    print(audio_to_text)

    return {
        "ayah_text": ayah_document["text"],
        "user_ayah":audio_to_text
    }
