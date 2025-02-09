from fastapi import FastAPI, Query
from services.openai_service import refine_query
from services.courtlistener_service import fetch_cases

app = FastAPI()

@app.get("/search")
async def search_cases(scenario: str = Query(..., description="Describe the legal scenario")):
    refined_query = refine_query(scenario)
    case_results = fetch_cases(refined_query)
    return {"cases": case_results}