import os
from yt_dlp import YoutubeDL
from flask import Flask, render_template, request, send_file
import time
import datetime
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    video_url = None

    def download_yt(url_input):
        nonlocal message
        options = {
            'outtmpl': 'video.mp4',
            'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]'
        }
        with YoutubeDL(options) as ydl:
            ydl.download([url_input])

    if request.method == 'POST':
        video_url = request.form.get('url')

    if request.method == 'POST' and video_url:
        try:
            download_yt(video_url)
            # No 'os' check here anymore! We just shoot the file straight to the browser.
            return send_file('video.mp4', as_attachment=True, download_name='video.mp4')
        except Exception as e:
            message = f"An error occurred during download: {e}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    # No 'os.environ' here either. We just use a standard port number.
    app.run(host='0.0.0.0', port=10000)
