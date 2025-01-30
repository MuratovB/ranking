from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from scrap_playlist import get_video_links
import random
import os
import json
import yt_dlp

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

cookies_data = os.getenv('YT_COOKIES')
cookies = json.loads(cookies_data) if cookies_data else []

app = FastAPI()
templates = Jinja2Templates(directory="api/templates")

# Helper function to fetch only video URLs
def get_video_urls(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Only extract URLs, no additional video info
        'cookiefile': None,  # Disable cookiefile, we are passing cookies directly
        'cookies': cookies,  # Pass cookies as a list
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(playlist_url, download=False)
            video_urls = [entry['url'] for entry in info_dict['entries']]
            return video_urls
        except Exception as e:
            return []  # Return empty list if any error occurs

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Default playlist URL (fallback)
    playlist_url = "https://www.youtube.com/playlist?list=PLItAIW8MhCBa2BQYeTK9kWGSRJ5jFn8CG"
    return templates.TemplateResponse("index.html", {"request": request, "playlist_url": playlist_url})

@app.post("/get_playlist/")
async def get_playlist(request: Request):
    form = await request.form()
    user_playlist_url = form.get('playlist_url', None)
    playlist_url = user_playlist_url if user_playlist_url else "https://www.youtube.com/playlist?list=PLItAIW8MhCBa2BQYeTK9kWGSRJ5jFn8CG"

    video_urls = get_video_urls(playlist_url)
    
    # Shuffle video URLs to ensure randomness
    random.shuffle(video_urls)

    # Pass the video URLs to the template
    return templates.TemplateResponse("rank.html", {"request": request, "videos": video_urls})

@app.post("/rank/")
async def rank(request: Request):
    form = await request.form()
    selected_video = form.get("selected_video")

    # Implement ranking logic here based on user selection

    return templates.TemplateResponse("rank.html", {"request": request, "videos": videos})

@app.get("/download")
async def download_ranking():
    # Assuming `ranked_videos` is a list of ranked URLs (not yet implemented)
    with open("ranking.txt", "w") as file:
        for i, video in enumerate(ranked_videos, 1):
            file.write(f"{i}, {video}\n")
    
    return FileResponse("ranking.txt", media_type='text/plain', filename='ranking.txt')
