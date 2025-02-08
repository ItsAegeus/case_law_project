# Backend (FastAPI + PostgreSQL) - Railway Deployment Ready
# This script sets up the API for case law search, integrating CourtListener and OpenAI GPT-4.

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests
import openai
import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8000))  # Railway assigns dynamic ports

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CaseLaw(Base):
    __tablename__ = "case_law"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    case_name = Column(String, nullable=False)
    citation = Column(String, nullable=True)
    court = Column(String, nullable=True)
    date_decided = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    full_case_url = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fetch case law from CourtListener
def fetch_case_law(query: str):
    url = f"https://www.courtlistener.com/api/rest/v3/search/?q={query}&type=o"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error retrieving case law")
    return response.json()

# AI-powered case summary
def generate_ai_summary(text: str):
    if not OPENAI_API_KEY:
        return "AI Analysis not available."
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal assistant that summarizes case law."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI API Error: {str(e)}")
        return "AI summary unavailable."

# API Endpoint for case search
@app.get("/search/")
def search_case(query: str, db: SessionLocal = Depends(get_db)):
    cached_case = db.query(CaseLaw).filter(CaseLaw.query == query).first()
    if cached_case:
        return cached_case
    
    case_data = fetch_case_law(query)
    if not case_data.get("results"):
        return {"message": "No cases found."}
    
    case = case_data["results"][0]  # Take first result
    summary = generate_ai_summary(case.get("caseName", ""))
    new_case = CaseLaw(
        query=query,
        case_name=case.get("caseName", "Unknown"),
        citation=case.get("citation", "N/A"),
        court=case.get("court", {}).get("name", "Unknown Court"),
        date_decided=case.get("dateFiled", "Unknown Date"),
        summary=summary,
        full_case_url=case.get("absolute_url", "")
    )
    db.add(new_case)
    db.commit()
    return new_case

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
