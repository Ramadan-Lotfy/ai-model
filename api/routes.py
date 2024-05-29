from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from db import database
from utils import similarity, speech, preprocessing
import random
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

router = APIRouter()

class QuestionResponse(BaseModel):
    questions: list[str]

class SpeechResponse(BaseModel):
    text: str

class AnswerModel(BaseModel):
    question: str
    answer: str

@router.get("/api/v1/select-questions/", response_model=QuestionResponse)
async def select_questions(dataset_name: str, num_questions: int):
    try:
        dataset_path = os.path.join(data_dir, dataset_name)
        if not os.path.exists(dataset_path):
            raise HTTPException(status_code=404, detail=f"Dataset file '{dataset_name}' not found")

        dataset = pd.read_csv(dataset_path)

        # Check if the requested number of questions exceeds the dataset size
        if num_questions > len(dataset):
            raise HTTPException(status_code=400, detail="Number of questions requested exceeds dataset size")

        # Select random questions from the dataset
        selected_questions = random.sample(dataset['Questions'].tolist(), num_questions)

        return {"questions": selected_questions}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception("An error occurred while processing the request:")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")

class AnswerInput(BaseModel):
    question: str
    answer: str

@router.post("/api/v1/submit-answer/", response_model=SpeechResponse)
async def submit_answer(answers: list[AnswerModel]):
    try:
        for i in range(len(answers)):
            processed_question = preprocessing.preprocess_text(answers[i].question)
            processed_answer = preprocessing.preprocess_text(answers[i].answer)

            similarity_score = similarity.calculate_cosine_similarity(processed_question, processed_answer)

            database.save_question_answer(answers[i].question, answers[i].answer, similarity_score)
        return {"similarity_score": similarity_score}
    except Exception as e:
        logger.exception("An error occurred while processing the request:")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")