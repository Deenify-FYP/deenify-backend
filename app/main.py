import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

import whisper
import whisper.audio

def patched_load_audio(file: str, sr: int = 16000):
    import subprocess
    import numpy as np
    cmd = [
        ffmpeg_path,
        "-nostdin", "-threads", "0", "-i", file,
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le",
        "-ar", str(sr), "-"
    ]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

whisper.audio.load_audio = patched_load_audio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import recitation

from transformers import RobertaForTokenClassification, AutoTokenizer

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.whisper_model = whisper.load_model("tiny")
    app.state.diacritizer_model = RobertaForTokenClassification.from_pretrained("guymorlan/levanti_arabic2diacritics")
    app.state.diacritizer_tokenizer = AutoTokenizer.from_pretrained("guymorlan/levanti_arabic2diacritics")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(recitation.router, prefix="/api", tags=["Recitation"])
