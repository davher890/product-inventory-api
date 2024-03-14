from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: str | None = None
    url: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
