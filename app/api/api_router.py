from fastapi import APIRouter

from app.routes.auth_route import router as auth_router
from app.routes.motivation_route import router as motivation_router
from app.routes.tips_route import router as tips_router
# PENTING: Jangan hapus ini, ini fitur ML/Prediksi kamu (dari HEAD)
from app.routes.predict_route import router as predict_router
# BARU: Import route untuk User Auth (dari Incoming/Teman)
from app.routes.user_auth_route import router as user_auth_router

api_router = APIRouter()

# Masukkan semua router
api_router.include_router(auth_router)       # Admin/General Auth
api_router.include_router(motivation_router) # Motivation
api_router.include_router(tips_router)       # Tips
api_router.include_router(predict_router)    # Predict (ML) -> Wajib ada
api_router.include_router(user_auth_router)  # User Auth -> Fitur baru