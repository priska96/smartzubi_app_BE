import os
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT", "dev")
dotenv_file = f".env.{environment}"
load_dotenv(dotenv_file)

class Config:
    YOUR_DOMAIN = os.environ.get('DOMAIN_URL') #os.getenv("DOMAIN_URL")
    STRIPE_KEY = os.environ.get('STRIPE_API_KEY_DEV') #os.getenv("STRIPE_API_KEY_DEV")
    ENVIRONMENT = "dev"#environment
    DB_HOSTNAME = os.environ.get('DB_HOSTNAME') #os.getenv("DB_HOSTNAME") 
    DB_PASSWORD = os.environ.get('DB_PASSWORD') #os.getenv("DB_PASSWORD")
    DATABASE_URL = "postgresql://"+os.environ.get('DATABASE_URL',"postgresql://"+ DB_HOSTNAME+":"+DB_PASSWORD+"@localhost/postgres").split("://")[1]