import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import urllib.request
import urllib.parse
import re
import os
import youtube

def search_youtube(event=None):
    """
    Searches YouTube based on the user's query and populates a listbox with the video titles.
    If an error occurs during the search, it updates the status label and shows an error message box.
    """
    to_search = search_entry.get()
    if not to_search:
        messagebox.showinfo("Error", "Please enter a search term.")
        return
    status_label.config(text="Searching...", fg='blue')
    query = urllib.parse.urlencode({'query': to_search})
    try:
        html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={query}&sp=EgIYAQ%253D%253D')
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if not video_ids:
            status_label.config(text="No videos found.", fg='red')
            return
        listbox.delete(0, tk.END)
        for video_id in list(set(video_ids)):
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            listbox.insert(tk.END, yt.title)
            videos_dict[yt.title] = yt
        status_label.config(text="Search completed. Select a video to download.", fg='green')
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to fetch videos: {e}")
        status_label.config(text="Search failed. Try again.", fg='red')

def download_video():
    """
    Downloads the selected video from the listbox in the highest available resolution to a pre-set download path.
    Displays a success message or an error message box depending on the outcome of the download attempt.
    """
    if not download_path:
        messagebox.showinfo("Error", "Please select a download directory.")
        return
    try:
        title = listbox.get(listbox.curselection())
        yt = videos_dict[title]
        yd = yt.streams.get_highest_resolution()
        yd.download(download_path)
        messagebox.showinfo("Success", f"Video downloaded successfully:\n{title}")
    except Exception as e:
        messagebox.showinfo("Error", f"Error downloading video: {e}")

def select_download_path():
    """
    Opens a dialog for the user to select a directory where videos will be downloaded.
    Saves the selected path globally and updates the path label on the GUI.
    """
    global download_path
    path = filedialog.askdirectory()
    if path:
        download_path = path
        youtube.save_download_path(download_path)
        path_label.config(text=f"Download Path: {download_path}")

root = tk.Tk()
root.title("YouTube Downloader=D")

# Set up the icon path dynamically to avoid hardcoding paths
script_dir = os.path.dirname(__file__)
icon_path = os.path.join(script_dir, 'logo.ico')
root.iconbitmap(icon_path)

videos_dict = {}
download_path = youtube.read_download_path()

# Initialize GUI elements
path_label = tk.Label(root, text=f"Download Path: {download_path if download_path else 'No Path Selected'}")
path_label.grid(row=0, column=1, padx=10, pady=10)

choose_path_button = tk.Button(root, text="Choose Download Path", command=select_download_path)
choose_path_button.grid(row=0, column=0, padx=10, pady=10)

search_entry = tk.Entry(root, width=50)
search_entry.grid(row=1, column=0, padx=10, pady=10)
search_entry.bind('<Return>', search_youtube)

search_button = tk.Button(root, text="Search", command=search_youtube)
search_button.grid(row=1, column=1, padx=10, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=2, column=0, columnspan=2)

listbox = tk.Listbox(root, width=100, height=10)
listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
