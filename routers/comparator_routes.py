import logging
import time

from fastapi import APIRouter, status
from pydantic import BaseModel
from starlette.responses import JSONResponse

from redis_connector import RedisConnector
from worker import store_words_to_redis

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


redis = RedisConnector()
store_words_to_redis.delay()


@router.get("/similar", status_code=200)
def similar(word: str) -> JSONResponse:
    """
    Handle request to search for words similar to passed word_to_compare.
    """
    start_time = time.perf_counter_ns()
    permutations = redis.get_word_permutations(word)
    permutations.remove(word)
    end_time = time.perf_counter_ns()
    process_time_ns = end_time - start_time
    redis.update_average_time(process_time_ns)
    return JSONResponse({SIMILAR: permutations})


@router.get("/stats", status_code=200, response_model=ResponseModel)
def stats() -> JSONResponse:
    """
    Return application statistics.
    """
    response_json = {
        "totalWords": redis.get_word_count(),
        "totalRequests": redis.get_total_requests(),
        "avgProcessingTimeNs": redis.get_average_process_time(),
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_json)
