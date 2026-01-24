from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
# from fastapi.middleware.cors import CORSMiddleware

from app.db import SessionLocal
from app import models, schemas
from app.utils import generate_short_code

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(payload: schemas.URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    url = models.URL(
        original_url=payload.original_url,
        short_code=short_code 
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return {
        "original_url": payload.original_url,
        "shorten_url": f"http://localhost:8000/{url.short_code}"
    }

@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(
        models.URL.short_code == short_code
    ).first()

    if not url: 
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url.original_url)

"""
@app.get('/')
def health():
    return {"status": "ok"}

@app.post('/shorten')
def shorten_url(url: str):
    return {
        "original_url": url,
        "short_url": "http://short.ly/abc123"
    }

@app.get("/db-check")
def db_check(db: Session=Depends(get_db)):
    return {"db": "connected"}

"""