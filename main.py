import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from config import config
from website import router as website_router
from scheduler import scheduler
import traceback
import asyncio
from creator import creator



logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(title='The Horoscope Project API')

app.mount("/static", StaticFiles(directory="static", follow_symlink=False), name="static")

app.include_router(website_router)

async def main() -> None:
    try:
        data_init = creator.initialize_data()
        if data_init is False:
            await creator.get_all_zodiacs_articles()
        scheduler.start()
        uvicorn_config = uvicorn.Config(app=app, host=config.HOST, port=int(config.PORT))
        server = uvicorn.Server(config=uvicorn_config)
        await server.serve()
        
        
        
        
    except Exception as e:
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    # uvicorn.run(
    #     # app,
    #     "main:app",
    #     host=config.HOST,
    #     port=int(config.PORT),
    #     reload=True
    # )
    try:
        asyncio.run(main())
    except Exception:
        logger.error(traceback.format_exc())