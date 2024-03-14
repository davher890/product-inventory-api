import logging

from sqlalchemy import Date, func, desc, case
from sqlalchemy.orm import Session

from models.product import Product
from schemas.product import ProductCreate

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def get_product_by_url(db: Session, url: str):
    return db.query(Product).filter(Product.url == url).first()


def get_brands(db: Session, source: str = None):
    brand_query = db.query(Product.brand).filter(Product.brand.isnot(None))
    if source is not None:
        brand_query = brand_query.filter(Product.spider_name == source)

    return [p.brand for p in brand_query.group_by(Product.brand).all()]


def get_categories(db: Session, source: str = None):
    category_query = db.query(Product.category).filter(Product.category.isnot(None))
    if source is not None:
        category_query = category_query.filter(Product.spider_name == source)

    return [p.category for p in category_query.group_by(Product.category).all()]


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    sort: str = None,
    source: str = None,
    brand: str = None,
    text: str = None,
    min_price: int = 0,
    category: str = None,
    update_date: str = None,
):
    product_query = db.query(Product).filter(Product.price > min_price)

    if source is not None:
        product_query = product_query.filter(Product.spider_name == source)

    if brand is not None:
        product_query = product_query.filter(func.lower(Product.brand) == brand.lower())

    if category is not None:
        product_query = product_query.filter(
            func.lower(Product.category) == category.lower()
        )

    if text is not None:
        product_query = product_query.filter(
            func.lower(Product.name).like(f"%{text.replace(' ', '%').lower()}%")
        )

    if update_date is not None:
        product_query = product_query.filter(
            Product.updated_at.cast(Date) == update_date
        )

    product_query = product_query.filter(Product.images.isnot(None))

    total = product_query.count()

    # if sort is not None:
    discount_order = desc(
        case(
            (
                Product.old_price > 0,
                100 * (Product.old_price - Product.price) / Product.old_price,
            ),
            else_=-1 * Product.price,
        )
    )

    product_query = product_query.order_by(discount_order)
    return {"total": total, "content": product_query.offset(skip).limit(limit).all()}


def create_product(db: Session, product: ProductCreate, user_id: int):
    db_product = Product(**product.dict(), owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
