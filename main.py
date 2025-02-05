from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from yt_dlp import YoutubeDL
import os
from fastapi import Request

# Initialize FastAPI app and Jinja2 template renderer
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Function to get video URLs, titles, and thumbnails from the YouTube playlist
def get_video_details(playlist_url: str):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,  # Extract video info, not just URLs
        'force_generic_extractor': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info_dict:
                # Extract details (URL, title, and thumbnail)
                video_details = [
                    {
                        'url': entry['url'],
                        'title': entry['title'],
                        'thumbnail': entry['thumbnails'][0]['url'] if 'thumbnails' in entry else None
                    }
                    for entry in info_dict['entries']
                ]
                return video_details
            else:
                raise HTTPException(status_code=400, detail="Invalid playlist URL")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to display the video details (URL, title, and thumbnail)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, playlist_url: str = ""):
    if playlist_url:
        # Fetch the video details from the playlist
        video_details = get_video_details(playlist_url)
        # Render HTML with the list of video details
        return templates.TemplateResponse("index.html", {"request": request, "video_details": video_details})
    return templates.TemplateResponse("index.html", {"request": request, "video_details": []})
