from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import glpi_auth_route

app = FastAPI(
    title="Dispatcher Backend",
    description="Middleware API for Dispatcher.",
    version="1.0.0"
)

# --- CORS Configuration ---
origins = [
    "http://localhost:4200", # Angular default
    "http://localhost:8100", # Ionic/Capacitor default
    "*"                      # Allow all (dev only)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(glpi_auth_route.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Dispatcher API is running"}

# If running via `python main.py` instead of `uvicorn main:app --reload`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)