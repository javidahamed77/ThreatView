from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserTier(enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class ThreatIndicator(Base):
    __tablename__ = 'threats'
    
    id = Column(Integer, primary_key=True)
    indicator = Column(String)
    type = Column(String)
    source = Column(String)
    confidence = Column(Integer)
    severity = Column(String)
    tags = Column(JSON, default=[])
    description = Column(String, default="")
    first_seen = Column(DateTime, default=datetime.now)
    last_seen = Column(DateTime, default=datetime.now)
    raw_data = Column(JSON)

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    threat_id = Column(Integer)
    alert_type = Column(String)
    message = Column(String)
    status = Column(String, default='new')
    created_at = Column(DateTime, default=datetime.now)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    tier = Column(Enum(UserTier), default=UserTier.FREE)
    api_key = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Existing fields
    company_name = Column(String)
    industry = Column(String)
    monitored_domains = Column(JSON, default=[])
    alert_email = Column(Boolean, default=True)
    alert_sms = Column(Boolean, default=False)