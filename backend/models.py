from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class CaseLaw(Base):
    __tablename__ = "case_laws"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    citation = Column(String, index=True)
    jurisdiction = Column(String, index=True)
    summary = Column(Text)
    full_text_url = Column(String)
