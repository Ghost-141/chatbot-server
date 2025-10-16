from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import logging

from api import api_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",  
)

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(api_router)

