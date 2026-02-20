from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ThreatIndicator, Alert  # 👈 Alert bhi import karo

DATABASE_URL = "sqlite:///./threatview.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(engine)

# For backward compatibility
Session = SessionLocal