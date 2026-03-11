from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "PLC SCL AI Generator"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./plc_scl.db")
    default_model: str = os.getenv("DEFAULT_MODEL", "local")


settings = Settings()
