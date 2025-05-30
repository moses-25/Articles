import os
from dotenv import load_dotenv

load_dotenv()
DB_CONF = {
    "host": os.getenv("PG_HOST"),
    "port": (os.getenv("PG_PORT") or "5432"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
}