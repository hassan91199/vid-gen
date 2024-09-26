import requests

from shortGPT.config.api_db import ApiKeyManager
from app.logger import logger

def search_youtube_videos(search_term):
    """
    Search for YouTube videos based on the given search term.
    
    Args:
        search_term (str): The search term to find videos.
        
    Returns:
        list or None: A list of video URLs or None if no videos are found or an error occurs.
    """
    
    url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        "part": "snippet",
        "q": search_term,
        "type": "video",
        "key": ApiKeyManager.get_api_key("YOUTUBE_API_KEY"),
        "maxResults": 10
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        video_results = response.json()
        if 'items' in video_results and video_results['items']:
            video_urls = [
                f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in video_results['items']
            ]
            logger.info(f"Found YouTube video URLs: {video_urls}")
            return video_urls
        else:
            logger.warning("No videos found for the given search term.")
            return None  # No videos found
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")
    
    return None  # Return None in case of an error