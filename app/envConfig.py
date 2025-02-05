import os
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT", "dev")
dotenv_file = f".env.{environment}"
load_dotenv(dotenv_file)

class Config:
    YOUR_DOMAIN = os.getenv("DOMAIN_URL")
    STRIPE_KEY = os.getenv("STRIPE_API_KEY_DEV")
    ENVIRONMENT = environment
    DB_HOSTNAME = os.getenv("DB_HOSTNAME") 
    DB_PASSWORD = os.getenv("DB_PASSWORD")
