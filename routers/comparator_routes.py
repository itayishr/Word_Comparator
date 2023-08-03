import logging
from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse
from pydantic import BaseModel

from worker import fetch_similar_words_task
SIMILAR = "similar"

# Configure logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Word Comparator"])


class ResponseModel(BaseModel):
    totalWords: int
    totalRequests: int
    avgProcessingTimeNs: int


@router.get("/similar", status_code=200)
async def similar(word_to_compare: str) -> JSONResponse:
    """
    Handle request to search for words similar to passed word_to_compare.
    """
    print("Got it!")
    similar_words = []
    fetch_similar_words_task.delay(word_to_compare)
    return JSONResponse({SIMILAR: similar_words})


@router.get("/stats", status_code=200, response_model=ResponseModel)
async def stats() -> JSONResponse:
    """
    Return application statistics. 
    """
    # TODO add stats logic.
    response_json = {"totalWords": 1, "totalRequests": 1, "avgProcessingTimeNs": 1}

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)
