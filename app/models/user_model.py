from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    userName = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    gender = Column(String(20))
    userDOB = Column(Date)
    
    # PERBAIKAN DI SINI:
    # Ganti avatarID (Integer) menjadi avatar (String) agar bisa menyimpan URL
    avatar = Column(String(255), nullable=True)