from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    API_URL = os.getenv("API_URL")

    ZODIACS = [
        'Aries',
        'Taurus',
        'Gemini',
        'Cancer',
        'Leo',
        'Virgo',
        'Libra',
        'Scorpio',
        'Sagittarius',
        'Capricorn',
        'Aquarius',
        'Pisces',
    ]

    # LOGIN = os.getenv("LOGIN")
    # PASSWORD = os.getenv("PASSWORD")

config = Config