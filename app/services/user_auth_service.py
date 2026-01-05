from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.user_auth_schema import UserRegister
# UPDATE: Import fungsi langsung, bukan class Hasher
from app.utils.hashing import hash_password, verify_password 

def create_user(db: Session, user_data: UserRegister):
    # Cek email/username duplikat
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.userName == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email atau Username sudah digunakan.")

    new_user = User(
        name=user_data.name,
        userName=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password), 
        gender=user_data.gender,
        userDOB=user_data.dob,
        
        # PERBAIKAN DI SINI:
        # Pastikan ini 'avatar', BUKAN 'avatarID'
        avatar=user_data.avatar 
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    
    # UPDATE: Menggunakan fungsi verify_password
    if not verify_password(password, user.password):
        return False
        
    return user