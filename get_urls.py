from yt_dlp import YoutubeDL
from fastapi import HTTPException

# Function to get video URLs from the YouTube playlist
def get_video_urls(playlist_url: str = 'https://www.youtube.com/playlist?list=PLItAIW8MhCBa2BQYeTK9kWGSRJ5jFn8CG'):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Don't download videos, just get URLs
        'force_generic_extractor': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info_dict:
                urls = [entry['url'] for entry in info_dict['entries']]
                return urls
            else:
                raise HTTPException(status_code=400, detail="Invalid playlist URL")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))