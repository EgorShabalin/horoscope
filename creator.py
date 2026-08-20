import logging
import httpx
import traceback
from config import config
import asyncio
import json
import os
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class Creator:
    my_api_url = config.API_URL

    httpx_client = httpx.AsyncClient(timeout=180)

    latest_horoscope_file = None
    horoscope_data = None


    async def get_current_timestamp(self) -> str:
        current_time = datetime.now() + timedelta(hours=3)
        current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        return current_time


    async def create_raw_article(
            self,
            zodiac: str,
            client: httpx.AsyncClient
    ) -> str:
        try:
            response = await client.post(
                url=self.my_api_url,
                params={
                    "text": f"""You are a professional astrologist.
    Create a professional horoscope for today for {zodiac}.
    Align the text as an article for a website.
    
    Don't write any title or date. Don't ask questions. Don't ask for more information.
    Your answer should only content an exact article with no other words.""",
                }, # The text should be about 500 symbols legth depending on important points you need to tell.
            )
            result = response.content.decode("utf-8")
            print(f"Raw text is ready:\n{result}\n")
        except Exception:
            full_exception = traceback.format_exc()
            return full_exception

        return result


    async def check_article_text(
            self,
            text: str,
            client: httpx.AsyncClient
    ) -> str:
        try:
            response = await client.post(
                url=self.my_api_url,
                params={
                    "text": f"""You are a professional writer. Check this article carefully.
    It should not content any title or date it was written.
    Check it for mistakes including logical or orfografic.
    Don't ask any questions or additional information.
    Return to me only edited text with no any comments.
    Here is the article I ask you to check: {text}""",
                },
            )
            result = response.content.decode("utf-8")
            print(f"The text has been checked:\n{result}\n")
        except Exception:
            full_exception = traceback.format_exc()
            return full_exception

        return result


    async def convert_to_html(
            self,
            text: str,
            client: httpx.AsyncClient
    ) -> str:
        try:
            response = await client.post(
                url=self.my_api_url,
                params={
                    "text": f"""You are a professional front-end developer.
    Convert this text to an html snippet like an article.
    It should not be a standalone webpage. It is only a part of the webpage.
    It should have this structure: <article>here_comes_the_article_it_self</article>.
    Remove all the '\n', use <p> instead.
    Don't ask any questions or additional information.
    Return to me only an html snippet.
    Here is the article text I ask you to convert to html: {text}""",
                },
            )
            result = response.content.decode("utf-8")
            print(f"Here comes the result:\n{result}\n")
        except Exception:
            full_exception = traceback.format_exc()
            return full_exception

        return result


    def clean_text(
            self,
            text: str | bytes
    ) -> str:
        try:
            if isinstance(text, bytes):
                text = text.decode("utf-8")
            text = str(text)
            text = text.replace('\\n', '')
            text = text.replace('\n', '')
            text = text.strip()
            if text.startswith('\"'):
                text = text[1:]
                text = text.strip()
            if text.endswith('\"'):
                text = text[:-1]
                text = text.strip()
            if text.startswith('"'):
                text = text[1:]
                text = text.strip()
            if text.endswith('"'):
                text = text[:-1]
                text = text.strip()
            return text
        except Exception:
            return traceback.format_exc()


    async def create_article(
            self,
            zodiac: str,
            client=httpx_client,
    ):
        raw_text = await self.create_raw_article(zodiac=zodiac, client=client)
        cheked_text = await self.check_article_text(text=raw_text, client=client)
        html_article = await self.convert_to_html(text=cheked_text, client=client)
        return html_article


    async def get_all_zodiacs_articles(self) -> dict:
        horoscope_dict = {}
        current_timestamp = await self.get_current_timestamp()
        async with self.httpx_client as client:
            tasks = [self.create_article(zodiac, client) for zodiac in config.ZODIACS]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        for zodiac, result in zip(config.ZODIACS, results):
            result = self.clean_text(text=result)
            horoscope_dict[zodiac] = result
        with open(file=f'horoscopes/{current_timestamp}_horoscope.txt', mode='w') as file:
            file.write(json.dumps(obj=horoscope_dict, indent=4, ensure_ascii=False))
        self.horoscope_data = horoscope_dict
        return horoscope_dict


    def get_latest_file(
            self,
            folder_path: str,
            suffix: str = "horoscope.txt"
    ) -> str | None:
        try:
            latest_time = datetime(year=2026, month=1, day=1, hour=0, minute=0)
            latest_filename = ''
            try:
                file_names = os.listdir(folder_path)
            except FileNotFoundError:
                return None
            for file_name in file_names:
                if not file_name.endswith(suffix):
                    continue

                time_str = file_name[:19]
                dt_time = datetime.strptime(time_str, "%Y-%m-%d_%H-%M-%S")
                if latest_time < dt_time:
                    latest_time = dt_time
                    latest_filename = file_name
            print(latest_filename)
            return latest_filename
        
        except Exception:
            full_traceback = traceback.format_exc()
            print(full_traceback)
            return None

    def get_horoscope_file_data(
            self,
            file_path: str
    ) -> dict:
        with open(file=file_path, mode='r') as file:
            horoscope_dict = json.loads(file.read())
        
        for k,v in horoscope_dict.items():
            print(f"{k} - {v[:50]}")
        return horoscope_dict

    def initialize_data(self) -> bool:
        self.latest_horoscope_file = self.get_latest_file(folder_path='horoscopes')
        if self.latest_horoscope_file:
            logger.info("Latest horoscopes data file found...")
            try:
                self.horoscope_data = self.get_horoscope_file_data(file_path=f'horoscopes/{self.latest_horoscope_file}')
                logger.info("Horoscopes data loaded...")
                return True
            except Exception:
                return False
        else:
            logger.info("Could not find latest horoscopes data file.")
        return False
            

creator = Creator()

# file =  asyncio.run(creator.get_latest_file(folder_path='horoscopes'))
# asyncio.run(creator.get_horoscope_file_data(file_path=f'horoscopes/{file}'))