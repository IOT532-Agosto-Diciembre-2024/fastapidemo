from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, Producto

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Producto).all()
    return products


class ProductoDTO(BaseModel):
    name: str
    description: str
    price: str
    weight: str


@app.post("/product")
async def create_product(producto: ProductoDTO, db: Session = Depends(get_db)):
    product = Producto(nombre= producto.name,descripcion=producto.description,precio=producto.price,peso=producto.weight)
    db.add(product)
    db.commit()
    return producto


@app.get("/product/{id}")
async def find_by_id(id: str, db: Session = Depends(get_db)):
    return db.query(Producto).filter(Producto.id==id).first()


