import os
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT", "dev")
dotenv_file = f".env.{environment}"
load_dotenv(dotenv_file)


class Config:
    YOUR_DOMAIN = os.environ.get("DOMAIN_URL")  # os.getenv("DOMAIN_URL")
    STRIPE_KEY = os.environ.get("STRIPE_API_KEY_DEV")  # os.getenv("STRIPE_API_KEY_DEV")
    ENVIRONMENT = "dev"  # environment
    DB_HOSTNAME = os.environ.get("DB_HOSTNAME")  # os.getenv("DB_HOSTNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")  # os.getenv("DB_PASSWORD")
    DATABASE_URL = (
        "postgresql://"
        + os.environ.get(
            "DATABASE_URL",
            "postgresql://" + DB_HOSTNAME + ":" + DB_PASSWORD + "@localhost/postgres",
        ).split("://")[1]
    )
    # JWT Config
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365  # 365 days
    REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365 * 1.5  # 1.5 years
    ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY", "narscbjim@$@&^@&%^&RFghgjvbdsha"
    )  # os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.environ.get(
        "JWT_REFRESH_SECRET_KEY", "13ugfdfgh@#$%^@&jkl45678902"
    )  # os.getenv("JWT_REFRESH_SECRET_KEY")
