from fastapi import FastAPI, Depends
import uvicorn
from backend.database import engine, Base, get_db
from backend.crud import search_case_law
from backend.schemas import CaseLawQuery, CaseLawResponse

app = FastAPI()

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

@app.post("/search/", response_model=CaseLawResponse)
def search_cases(query: CaseLawQuery, db=Depends(get_db)):
    return search_case_law(db, query)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
