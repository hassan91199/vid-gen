import moviepy.editor as mp
import requests
from PIL import Image
from io import BytesIO
import os
import time

def download_image(image_url, output_path):
    """Download image from URL and save it to the output path."""
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(output_path)
    return output_path

def create_static_video(image_path, duration):
    """Create a static video from an image for the specified duration."""
    clip = mp.ImageClip(image_path).set_duration(duration)
    
    # Set the position to keep it centered
    clip = clip.set_position("center")
    
    return clip

def convert_images_to_videos(image_data, output_dir="output_videos"):
    """Convert image URLs into separate videos without zoom effects."""
    output_videos = []

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    temp_image_path = 'videos/temp_images'

    # Create temporary folder for downloaded images
    if not os.path.exists(temp_image_path):
        os.makedirs(temp_image_path)

    for idx, (time_range, image_url) in enumerate(image_data):
        start_time, end_time = time_range
        duration = end_time - start_time

        # Download image and save it locally
        temp_image_timestamp = int(time.time())
        image_path = download_image(image_url, f'{temp_image_path}/temp_image_{temp_image_timestamp}.png')

        # Create a static video clip
        video_clip = create_static_video(image_path, duration)
        
        # Set video file path
        timestamp = int(time.time())
        video_filename = f"{output_dir}/video_{timestamp}.mp4"

        # Write the static video to the file
        video_clip.write_videofile(video_filename, codec='libx264', fps=24)

        # Append time range and video URL to the output
        output_videos.append([time_range, video_filename])

    # Clean up the temporary images
    for img in os.listdir(temp_image_path):
        os.remove(os.path.join(temp_image_path, img))
    os.rmdir(temp_image_path)

    return output_videos