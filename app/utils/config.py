from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PWD: str
    DB_NAME: str
    
    JWT_SECRET_KEY: str
    JWT_TOKEN_TIMEOUT: int = 60 * 24 * 7
    
    class Config:
        env_file = ".env"
    
settings = Settings()