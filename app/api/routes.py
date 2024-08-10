from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "Healthy"}

@router.get("/hello")
def hello():
    return {"message": "Hello"}