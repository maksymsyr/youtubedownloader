import sys
import os
import urllib.request
import urllib.parse
import re
from pytube import YouTube

def read_download_path():
    """Reads the download path from a file."""
    try:
        script_dir = os.path.dirname(__file__)
        path_file = os.path.join(script_dir, 'download_path.txt')
        with open(path_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_download_path(path):
    """Saves the download path to a file."""
    script_dir = os.path.dirname(__file__)
    path_file = os.path.join(script_dir, 'download_path.txt')
    with open(path_file, 'w') as file:
        file.write(path)

def main():
    if len(sys.argv) < 2:
        sys.exit("Oops! You didn't provide a search term.")

    # Combines all parts of the search term (in case of multi-word search terms)
    to_search = ' '.join(sys.argv[1:])
    query = urllib.parse.urlencode({'search_query': to_search})
    url = f'https://www.youtube.com/results?{query}&sp=EgIYAQ%253D%253D'

    try:
        html = urllib.request.urlopen(url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if not video_ids:
            sys.exit("No videos found.")

        # Assuming only the first found video is relevant
        yt = YouTube(f"https://www.youtube.com/watch?v={video_ids[0]}")
        print(f"Title: {yt.title}")

        # Select the highest resolution stream available
        yd = yt.streams.get_highest_resolution()
        download_path = read_download_path() or 'C:\\Users\\maksy\\Desktop\\videos'
        yd.download(download_path)
        print(f"Video downloaded to: {download_path}")

    except Exception as e:
        sys.exit(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
