from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from scrap_playlist import get_video_links
from dotenv import load_dotenv
import random
import os
import json
import yt_dlp

load_dotenv()
cookies_data = os.getenv('YT_COOKIES')
if cookies_data:
    cookies = json.loads(cookies_data)
else:
    cookies = []

app = FastAPI()

templates = Jinja2Templates(directory="api/templates")


# Helper function to handle odd number of videos
def handle_odd_video_round(videos):
    # If the number of videos is odd, take the first video and move it to the next round
    if len(videos) % 2 != 0:
        winner_video = videos.pop(0)  # Remove the first video and save it
        return videos, winner_video  # Return the remaining videos and the winner to move forward
    return videos, None  # If even number of videos, no special handling needed


# Helper function to format the results into a list of dictionaries, including fetching titles
def get_video_details(urls):
    video_details = []
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # We only want to extract the video info, not the full video
        'cookiefile': None,  # Disable cookiefile, we are passing cookies directly
        'cookies': cookies,  # Pass cookies as a list
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                # Extract video info using yt-dlp
                info_dict = ydl.extract_info(url, download=False)
                
                # Extract title and thumbnail from the video info
                title = info_dict.get("title", "No Title Found")
                video_id = info_dict.get("id", "")
                thumbnail = f"https://img.youtube.com/vi/{video_id}/0.jpg"  # Thumbnail URL

                video_details.append({
                    "url": url,
                    "title": title,
                    "thumbnail": thumbnail
                })
            except Exception as e:
                # If we can't fetch info, append default info
                video_details.append({
                    "url": url,
                    "title": "Failed to fetch title",
                    "thumbnail": "https://via.placeholder.com/150"  # Default placeholder image
                })
    return video_details


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

    try:
        video_urls = get_video_links(playlist_url=playlist_url)
    except Exception:
        video_urls = get_video_links()

    # Shuffle video URLs to ensure randomness
    random.shuffle(video_urls)

    # Get video details (title and thumbnail for display)
    videos = get_video_details(video_urls)
    
    # Handle odd number of videos
    videos, winner_video = handle_odd_video_round(videos)

    return templates.TemplateResponse("rank.html", {"request": request, "videos": videos, "winner_video": winner_video})


@app.post("/rank/")
async def rank(request: Request):
    form = await request.form()
    # Assuming user has chosen which video is better in the previous ranking pair
    selected_video = form.get("selected_video")

    # Update ranking logic here based on the user's choice
    # You'd also need to implement logic to move to the next pair of videos, handle odd/even rounds, etc.

    return templates.TemplateResponse("rank.html", {"request": request, "videos": videos})

@app.get("/download")
async def download_ranking():
    with open("ranking.txt", "w") as file:
        for i, video in enumerate(ranked_videos, 1):
            file.write(f"{i}, {video['title']}, {video['url']}\n")
    
    return FileResponse("ranking.txt", media_type='text/plain', filename='ranking.txt')
