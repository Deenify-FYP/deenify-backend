import httpx
from fastapi import HTTPException

async def fetch_ayah_data(ayah_number: int, surah_number: int, api_url: str):
    reference = f"{surah_number}:{ayah_number}"
    if not api_url.endswith("/"):
        api_url += "/"
    full_url = f"{api_url}{reference}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(full_url)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"API error: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Request error: {str(e)}"
        )

    return data
