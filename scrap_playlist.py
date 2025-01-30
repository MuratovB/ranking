from pytube import Playlist

def get_video_links(playlist_url='https://www.youtube.com/playlist?list=PLItAIW8MhCBa2BQYeTK9kWGSRJ5jFn8CG'):
    # Create a Playlist object
    playlist = Playlist(playlist_url)

    # Extract all video URLs in the playlist
    video_urls = playlist.video_urls
    
    return video_urls
