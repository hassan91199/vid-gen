import requests
import os
import time
import subprocess

def download_image(image_url, output_path):
    """Download image from URL and save it to the output path."""
    response = requests.get(image_url)
    with open(output_path, 'wb') as f:
        f.write(response.content)
    return output_path

def create_video_with_zoom(image_path, duration, output_path):
    """Create a video with a zoom effect using FFmpeg."""
    # Build the FFmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-loop', '1',                       # Loop the image
        '-i', image_path,                   # Input image
        '-vf', f"zoompan=z='if(lte(in,{duration * 25}),zoom+0.002,zoom-0.002)':d={int(25 * duration)}:s=1024x1024:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=25",
        '-c:v', 'libx264',                  # Video codec
        '-t', str(duration),                 # Duration of the output video
        '-s', '1024x1024',                  # Output resolution
        '-pix_fmt', 'yuv420p',              # Pixel format
        '-y',                                # Overwrite output file if it exists
        output_path                          # Output video file
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

def convert_images_to_videos(image_data, output_dir="output_videos"):
    """Convert image URLs into separate videos with zoom effects."""
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

        # Set video file path
        timestamp = int(time.time())
        video_filename = f"{output_dir}/video_{timestamp}.mp4"

        # Create a video with zoom effect using FFmpeg
        create_video_with_zoom(image_path, duration, video_filename)

        # Append time range and video URL to the output
        output_videos.append([time_range, video_filename])

    # Clean up the temporary images
    for img in os.listdir(temp_image_path):
        os.remove(os.path.join(temp_image_path, img))
    os.rmdir(temp_image_path)

    return output_videos