from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from yt_dlp import YoutubeDL
import os
from fastapi import Request

# Initialize FastAPI app and Jinja2 template renderer
app = FastAPI()
templates = Jinja2Templates(directory="templates")

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

# Route to display the video URLs
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, playlist_url: str = ""):
    if playlist_url:
        # Fetch the video URLs from the playlist
        video_urls = get_video_urls(playlist_url)
        # Render HTML with the list of video URLs as <a> tags
        return templates.TemplateResponse("index.html", {"request": request, "video_urls": video_urls})
    return templates.TemplateResponse("index.html", {"request": request, "video_urls": []})

