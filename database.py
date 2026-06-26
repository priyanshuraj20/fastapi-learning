from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

db_url = "postgresql://postgres:Priyanshu1234@localhost:5432/demo"

engine = create_engine(db_url)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Add this utility dependency generator
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
