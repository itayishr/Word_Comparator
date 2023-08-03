from fastapi import FastAPI
from routers import comparator_routes
import uvicorn

app = FastAPI(
    title="Word Comparator Rest API",
    description="Word Comparator service implemented with FastAPI, to supply the Word Comparator with new requests.",
    version="1.0.0",
)
app.include_router(comparator_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
