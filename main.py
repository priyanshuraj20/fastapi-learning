from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Product  # Your Pydantic model
from database import sessionLocal, engine, get_db
import database_models  # Your SQLAlchemy models

app = FastAPI()

# 1. Automatically build tables when app starts
database_models.Base.metadata.create_all(bind=engine)

# 2. Hardcoded local data list used ONLY for seeding database initial values
initial_products = [
    Product(id=1, name="phone", description="budget Phone", price=90, quantity=24),
    Product(id=2, name="phone1", description="budget Phone", price=99, quantity=10)
]

# Lifespan startup script to check/seed database exactly once
@app.on_event("startup")
def seed_database():
    db = sessionLocal()
    try:
        for prod in initial_products:
            exists = db.query(database_models.Product).filter_by(id=prod.id).first()
            if not exists:
                db.add(database_models.Product(**prod.model_dump()))
        db.commit()
        print("Database checked and seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Seed Error: {e}")
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "hello learning fastApi"}

#By using Depends(get_db), FastAPI guarantees that each incoming request gets its own completely isolated database session.
# READ ALL FROM DATABASE
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # Query all records out of the PostgreSQL 'product ' table
    db_products = db.query(database_models.Product).all()
    return db_products


# READ ONE FROM DATABASE
@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")
    return product


# CREATE (WRITE TO DATABASE)
@app.post("/product", status_code=status.HTTP_201_CREATED)
def add_product(product: Product, db: Session = Depends(get_db)):
    # Check if ID already exists to prevent unique constraint crashes
    exists = db.query(database_models.Product).filter_by(id=product.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Product ID already exists!")
        
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# UPDATE IN DATABASE
@app.put("/product/{id}")
def update_the_product(id: int, updated_data: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="No product found!")

    # Explicitly update fields on our active database tracking instance
    db_product.name = updated_data.name
    db_product.description = updated_data.description
    db_product.price = updated_data.price
    db_product.quantity = updated_data.quantity

    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "data": db_product}


# DELETE FROM DATABASE
@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found!")
        
    db.delete(db_product) # Removes the row completely from the database tracking index
    db.commit()          # Pushes structural deletion to PostgreSQL
    return {"message": f"Product with ID {id} deleted successfully"}
