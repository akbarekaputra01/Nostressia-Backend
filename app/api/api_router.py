from fastapi import APIRouter

# 1. Import route yang sudah ada (Admin, Motivasi, Tips)
from app.routes.auth_route import router as auth_router
from app.routes.motivation_route import router as motivation_router
from app.routes.tips_route import router as tips_router

# 2. BARU: Import route untuk User Auth
# PERHATIKAN: Kita import 'router' dari file 'user_auth_route', BUKAN schema-nya.
from app.routes.user_auth_route import router as user_auth_router

api_router = APIRouter()

# 3. Masukkan route ke router utama
api_router.include_router(auth_router)       # Admin Auth (biasanya prefix /auth)
api_router.include_router(motivation_router) # Motivation
api_router.include_router(tips_router)       # Tips
api_router.include_router(user_auth_router)  # User Auth (Login/Register User -> prefix /user)