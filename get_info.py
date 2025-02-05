import requests
from bs4 import BeautifulSoup as bs

def get_video_info(url: str = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'):
    # Send GET request to the YouTube video URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        
        # Extract the title from the <title> tag
        title = soup.find('title').text.strip()

        # Extract the thumbnail from the <meta> tag with property="og:image"
        thumbnail = soup.find('meta', property='og:image')
        if thumbnail:
            thumbnail_url = thumbnail.get('content')
        else:
            thumbnail_url = None
        print(f"Title: {title}\nThumbnail: {thumbnail}")
        return title, thumbnail_url
    else:
        return None, None
