import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.vid_gen import VidGen

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DescriptionRequest(BaseModel):
    description:str

@router.get("/health")
def health_check():
    return {"status": "Healthy"}

@router.get("/hello")
def hello():
    return {"message": "Hello"}

@router.post("/vid-gen")
async def vid_gen(description_request: DescriptionRequest):
    try:
        vidgen = VidGen()

        script = vidgen.generate_script(description_request.description)

        video_path = vidgen.make_video()

        # Log the video path
        logger.info(f"Video created at: {video_path}")

        return {"path": video_path}
    except Exception as e:
        # Log the error with stack trace
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
