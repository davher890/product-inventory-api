from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from services.product import get_products, get_brands, get_categories

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/brands")
def read_brands(source: str = None, db: Session = Depends(get_db)):
    return get_brands(db, source=source)


@app.get("/categories")
def read_categories(source: str = None, db: Session = Depends(get_db)):
    return get_categories(db, source=source)


@app.get("/products")
def read_products(
    page: int = 0,
    limit: int = 20,
    source: str = None,
    brand: str = None,
    text: str = None,
    min_price: int = 0,
    category: str = None,
    update_date: str = None,
    sort: str = None,
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    products = get_products(
        db,
        skip=skip,
        limit=limit,
        sort=sort,
        source=source,
        brand=brand,
        text=text,
        category=category,
        min_price=min_price,
        update_date=update_date,
    )
    return products
