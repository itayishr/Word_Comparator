import logging
from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse
from pydantic import BaseModel

SIMILAR = "similar"

# Configure logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/v1', tags=['Word Comparator'])


class ResponseModel(BaseModel):
    totalWords: int
    totalRequests: int
    avgProcessingTimeNs: int
 
@router.get("/similar", status_code=200)
async def similar(word_to_compare: str) -> JSONResponse:
    """
    Handle request to search for words similar to passed word_to_compare.
    """
    similar_words = []
    return JSONResponse({SIMILAR: similar_words})


@router.get("/stats", status_code=200,response_model=ResponseModel)
async def stats() -> JSONResponse:
    """
    Handle request to search for words similar to passed word_to_compare.
    """
    similar_words = []
    return JSONResponse({SIMILAR: similar_words})