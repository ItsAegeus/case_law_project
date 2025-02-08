from sqlalchemy.orm import Session
from backend.models import CaseLaw
import backend.courtlistener as courtlistener
from backend.schemas import CaseLawQuery, CaseLawResponse


def search_case_law(db: Session, query: CaseLawQuery):
    cached_case = db.query(CaseLaw).filter_by(jurisdiction=query.jurisdiction, title=query.keywords).first()
    
    if cached_case:
        return CaseLawResponse(
            title=cached_case.title,
            citation=cached_case.citation,
            jurisdiction=cached_case.jurisdiction,
            summary=cached_case.summary,
            full_text_url=cached_case.full_text_url,
        )
    
    case = courtlistener.fetch_case_law(query.keywords, query.jurisdiction)
    
    if case:
        new_case = CaseLaw(
            title=case["title"],
            citation=case["citation"],
            jurisdiction=case["jurisdiction"],
            summary=case["summary"],
            full_text_url=case["full_text_url"],
        )
        db.add(new_case)
        db.commit()
        db.refresh(new_case)

        return CaseLawResponse(**case)

    return None
