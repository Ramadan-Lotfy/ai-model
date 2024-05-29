# db.models.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QuestionAnswer(Base):
    __tablename__ = 'question_answers'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    user_answer = Column(String)
    score = Column(Float)