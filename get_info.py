import requests
from bs4 import BeautifulSoup as bs

def get_video_info(url):
    # Send GET request to the YouTube video URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        
        # Extract the title from the <div> tag with id="title"
        title_div = soup.find('div', {'id': 'title'})
        if title_div:
            title = title_div.get_text(strip=True)
        else:
            title = None

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
