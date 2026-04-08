from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import auth_routes, scan_routes, admin_routes
import os

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dependency Scanner")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_routes.router)
app.include_router(scan_routes.router)
app.include_router(admin_routes.router)

# Mount Frontend (Static Files)
# Ensure the directory exists
if not os.path.exists("frontend"):
    os.makedirs("frontend")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
