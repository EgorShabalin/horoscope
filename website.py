import logging
import traceback
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, HTTPException, Depends
from config import config
from creator import creator


logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

async def get_locale(request: Request) -> dict:
    accept_lang = request.headers.get("accept-language")
    logger.info(f"ACCEPT_LANGUAGE: {accept_lang}")
    return accept_lang

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    lang=Depends(get_locale)
):
    try:
        current_lang = str(lang)[:2]
        return RedirectResponse(
            url=f'/{current_lang}'
        )
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )


@router.get("/{lang}", response_class=HTMLResponse)
async def home(
    request: Request,
    lang: str,
):
    try:
        current_date = creator.horoscope_data.get(f'current_date').get(f'{lang}')
        zodiacs = config.ZODIACS
        return templates.TemplateResponse(
                request=request,
                context={
                    "zodiacs": zodiacs,
                    "date": current_date,
                    "lang": lang,
                },
                name='home.html',
            )
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )
    

@router.get("/{zodiac}/{lang}", response_class=HTMLResponse)
async def sagittarius(
    zodiac: str,
    lang: str,
    request: Request,
):
    try:
        if creator.horoscope_data:
            logger.debug(f"Horoscopes data: {creator.horoscope_data.keys()}")
            text = creator.horoscope_data.get(zodiac.capitalize()).get(lang)
        else:
            text = 'No data'
        if not lang == 'en':
            zodiac_name = config.ZODIACS.get(zodiac.capitalize())[lang]
        else:
            zodiac_name = zodiac

        return templates.TemplateResponse(
                request=request,
                name="zodiac.html",
                context={
                    "zodiac": zodiac_name,
                    "text": text,
                    "lang": lang,
                },
            )
    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )