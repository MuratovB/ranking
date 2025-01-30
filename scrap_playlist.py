import yt_dlp

def get_video_links(playlist_url='https://www.youtube.com/playlist?list=PLItAIW8MhCBa2BQYeTK9kWGSRJ5jFn8CG'):
    ydl_opts = {
        'extract_flat': True,  # Avoid downloading videos, just get the links
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        video_urls = [entry['url'] for entry in info_dict['entries']]
    return video_urls
