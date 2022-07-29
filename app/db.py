import psycopg2

from app.utils.config import settings

conn = psycopg2.connect(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PWD,
    dbname=settings.DB_NAME,
)
