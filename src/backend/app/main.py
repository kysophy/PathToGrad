from fastapi import FastAPI

from app.api import academic_record
from app.api import meta
from app.api import profile


app = FastAPI(
    title="PathToGrad API",
    version="0.1.0",
)

@app.get("/")
@app.get("/api/health")
def health_check():
    return {
        "status": "ok"
    }


app.include_router(
    meta.router
)

app.include_router(
    profile.router
)

app.include_router(
    academic_record.router
)
