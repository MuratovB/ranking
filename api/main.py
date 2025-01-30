from fastapi import FastAPI
from scrap_playlist import get_video_links

app = FastAPI()

@app.get('/')
def home():
  return get_video_links()
