import os
from yt_dlp import YoutubeDL
from flask import Flask, render_template, request
import time
import datetime
app = Flask(__name__)






@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    video_url = None
    def download_yt(video_url):
        nonlocal message

        nonlocal options
        try:
            with YoutubeDL(options) as ydl:
                ydl.download([video_url])

                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)

                return filename

        except Exception as e:
            message = f"Error occurred: {e}"
    options = {
        # IMPORTANT: This must point to the 'bin' folder of the EXTRACTED ffmpeg folder, not the .7z/.tar.xz file!
        'ffmpeg_location': 'C:\\Users\\doodo\\Downloads\\ffmpeg-8.1.1-full_build\\ffmpeg-8.1.1-full_build\\bin',
        'outtmpl': 'C:/Users/doodo/Downloads/%(title)s.%(ext)s',
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]'  # Forces it to be a clean MP4 instead of Opera webm file
    }

    if request.method == 'POST':
        video_url = request.form.get('url')


    # Grab visitor details
    visitor_ip = request.remote_addr
    visitor_device = request.headers.get('User-Agent', 'Unknown Device')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



    try:
        with open("visitor_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"--- NEW VISITOR LOG ---\n")
            log_file.write(f"Time: {current_time}\n")
            log_file.write(f"IP Address: {visitor_ip}\n")
            log_file.write(f"Device Info: {visitor_device}\n")
            if visitor_ip ==  '127.0.0.1':
                log_file.write("my ip address (127.0.0.1)")
            if video_url:
                log_file.write(f"Action: Downloaded URL -> {video_url}\n")
            log_file.write("\n")
    except Exception as log_error:
        print(f"Log file error: {log_error}")

    # Handle the download if a form was submitted
    if request.method == 'POST' and video_url:
        try:
            download_yt(video_url)
            if download_yt(video_url):
                message = "Successfully downloaded"
        except Exception as e:
            message = f"An error occurred during download: {e}"


    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
# video_url = input("Enter your url: ")
# def download_yt(video_url):
#     options= {
#         'ffmpeg_location': 'C:\\Users\\doodo\\Downloads\\ffmpeg-8.1.1.tar.xz',
#             'outtmpl': 'C:/Users/doodo/Downloads/%(title)s.%(ext)s',  # Saves the file using the YouTube video's actual title
#          }
#     try:
#         with YoutubeDL(options) as ydl:
#             ydl.download([video_url])
#             info = ydl.extract_info(video_url, download=True)
#             filename = ydl.prepare_filename(info)
#             return filename
#         print("downloaded")
#     except Exception as e:
#         message = f"Error occurred: {e}"
#
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     message = ""
#     visitor_ip = request.remote_addr
#     visitor_device = request.headers.get('User-Agent')
#     current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     with open("visitor_log.txt", "a", encoding="utf-8") as log_file:
#         log_file.write(f"--- NEW VISITOR LOG ---\n")
#         log_file.write(f"Time: {current_time}\n")
#         log_file.write(f"IP Address: {visitor_ip}\n")
#         log_file.write(f"Device Info: {visitor_device}\n")
#         if request.method == 'POST':
#             video_url = request.form.get('url')
#             log_file.write(f"Action: Downloaded URL -> {video_url}\n")
#         log_file.write("\n")
#         if video_url:
#             try:
#
#                 download_yt(video_url)
#                 message = "Success! Video downloaded."
#             except Exception as e:
#                 message = f"An error occurred: {e}"
#     return render_template('index.html', message=message)
# print(download_yt(video_url))
# if __name__ == '__main__':
#     app.run(debug=True, port=8080)