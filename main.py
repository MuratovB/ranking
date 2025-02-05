from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from get_urls import get_video_urls
from get_info import get_video_info

# Initialize FastAPI app and Jinja2 template renderer
app = FastAPI()
templates = Jinja2Templates(directory="templates")
get_video_info()

# Route to display the video URLs
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, playlist_url: str = ""):
    if playlist_url:
        # Fetch the video URLs from the playlist
        video_urls = get_video_urls(playlist_url)
        # Render HTML with the list of video URLs as <a> tags
        return templates.TemplateResponse("index.html", {"request": request, "video_urls": video_urls})
    return templates.TemplateResponse("index.html", {"request": request, "video_urls": []})

