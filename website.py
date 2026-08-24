import logging
import traceback
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, HTTPException
from config import config
from creator import creator


logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
):
    try:
        current_date = creator.horoscope_data.get('current_date_en')
        return templates.TemplateResponse(
                request=request,
                context={
                    "zodiacs": config.ZODIACS.keys(),
                    "date": current_date,
                },
                name='home.html',
            )
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )
    

@router.get("/{zodiac}", response_class=HTMLResponse)
async def sagittarius(
    zodiac: str,
    request: Request,
):
    try:
        if creator.horoscope_data:
            logger.debug(f"Horoscopes data: {creator.horoscope_data.keys()}")
            text = creator.horoscope_data.get(zodiac.capitalize())
        else:
            text = 'No data'

        return templates.TemplateResponse(
                request=request,
                name="zodiac.html",
                context={
                    "zodiac": zodiac,
                    "text": text,
                },
            )
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )