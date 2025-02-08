from pydantic import BaseModel

class CaseLawQuery(BaseModel):
    keywords: str
    jurisdiction: str

class CaseLawResponse(BaseModel):
    title: str
    citation: str
    jurisdiction: str
    summary: str
    full_text_url: str
