from fastapi import UploadFile,HTTPException,Request
import tempfile
import os
import whisper

async def transcribe_audio(request:Request,upload_file:UploadFile):
    model:whisper.Whisper = request.app.state.model

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    #Saving the file on the server first
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        contents = await upload_file.read()
        temp.write(contents)
        temp.flush()
        temp_name = temp.name

    try:
        #Converting audio to text
        result = model.transcribe(temp_name, language="ar")
        return result["text"]
    finally:
        #Deleting the audio file from server
        if os.path.exists(temp_name):
            os.remove(temp_name)
