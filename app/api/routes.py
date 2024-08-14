import logging
from fastapi import BackgroundTasks, APIRouter, HTTPException
from pydantic import BaseModel
from app.vid_gen import VidGen
from shortGPT.gpt import gpt_yt
from shortGPT.database.content_database import ContentDatabase

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
async def vid_gen(description_request: DescriptionRequest, background_tasks: BackgroundTasks):
    try:
        vidgen = VidGen()

        content_db = ContentDatabase()
        content_data_manager = content_db.createContentDataManager("general_video")
        video_id = content_data_manager._getId()

        vidgen.video_id = video_id

        script = vidgen.generate_script(description_request.description)

        title, caption = gpt_yt.generate_title_description_dict(script)

        background_tasks.add_task(vidgen.make_video)

        return {
            "video_id": video_id,
            "title": title,
            "caption": caption,
            "script": script
        }
    except Exception as e:
        # Log the error with stack trace
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
