# This Code Made by D3F417
# Github : https://github.com/mss-d3f417
# Don't Copy Script KIDI 

from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import tkinter.font as font
import requests
import validators
import os
from urllib.parse import urlparse
import threading
from tqdm import tqdm  # Make sure to install tqdm using 'pip install tqdm'

root = Tk()
root.title("D3F417 Downloader | GUI App")
icon = PhotoImage(file='icon.png')
root.iconphoto(False, icon)
root.geometry("600x500")
root.resizable(False, False)
FONT = font.Font(family="Helvetica", size="10", weight="bold")


canvas = Canvas(root, height=500, width=600)
canvas.pack()
background_image = ImageTk.PhotoImage(Image.open("bg.jpg"))
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)


frame = Frame(root, bg="#445256", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.15, anchor="n")

label_up = Label(frame, text="D3F417 Downloader", font=("Helvetica", 16, "bold"), bg="#445256", fg="white")
label_up.place(relwidth=1, relheight=0.5)

label1 = Label(frame, text="Enter the URL", font=FONT, bd=5, bg="#445256", fg="white")
label1.place(relx=0.1, rely=0.6, relwidth=0.25, relheight=0.3)

entry1 = Entry(frame, font=FONT, fg="#2c3e50")
entry1.place(relx=0.4, rely=0.6, relwidth=0.5, relheight=0.3)


button1 = Button(root, text="DOWNLOAD", font=FONT, bg="#2ecc71", fg="white",
                 activeforeground="#2ecc71", activebackground="#34495e",
                 command=lambda: threading.Thread(target=lambda: download(entry1.get())).start())
button1.place(relx=0.25, rely=0.3, relwidth=0.19, relheight=0.07)


def clear():
    entry1.delete(0, END)
    label_down['text'] = ""
    progress_bar["value"] = 0

button2 = Button(root, text="CLEAR", font=FONT, bg="#e74c3c", fg="white",
                 activeforeground="#e74c3c", activebackground="#34495e", command=clear)
button2.place(relx=0.55, rely=0.3, relwidth=0.19, relheight=0.07)


progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.place(relx=0.5, rely=0.8, anchor="center")

def download(url):
    valid = validators.url(url)

    if not valid:
        messagebox.showerror("Invalid URL", "URL is invalid")
    elif url == "":
        messagebox.showerror("No valid URL", "URL cannot be empty")
    else:
        response = requests.get(url, stream=True)

        if canbedownloaded(response.headers['Content-Type']):
            a = urlparse(url)
            name = os.path.basename(a.path)
            filename = 'D3F417-' + name
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded = 0

            with open(filename, 'wb') as f:
                for data in tqdm(response.iter_content(block_size), total=total_size, unit='B', unit_scale=True,
                                 desc=filename, ncols=90):
                    f.write(data)
                    downloaded += len(data)

                    
                    progress_bar["value"] = (downloaded / total_size) * 100
                    root.update_idletasks()

            label_down['text'] = f"Your file {filename}\n has been downloaded successfully."
        else:
            label_down['text'] = "This file is invalid. It cannot be downloaded."

def canbedownloaded(content_type):
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        return False
    return True

root.mainloop()