from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.base import settings

DATABASE_URL = settings.database_url
IMAGE_STORAGE_CONNECTION_STRING = f"DefaultEndpointsProtocol={settings.DefaultEndpointsProtocol};AccountName={settings.AccountName};AccountKey={settings.AccountKey};EndpointSuffix={settings.EndpointSuffix}"
IMAGE_PATH = settings.image_path

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

if "None" in IMAGE_STORAGE_CONNECTION_STRING:
    # check if there is an image directory, if not create one
    import os

    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
