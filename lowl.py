from flask import Flask, request, render_template, send_from_directory
import os
from pytube import YouTube

app = Flask(__name__)

# Directory where the downloaded audio will be stored
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_audio(url):
    # Create a YouTube object
    yt = YouTube(url)

    # Accessing streaming data
    metadata = yt.streaming_data
    adaptive_formats_list = metadata.get("adaptiveFormats")

    # Filter list of dictionaries for audio-only streams
    audio_streams = [stream for stream in adaptive_formats_list if stream['mimeType'].startswith('audio/')]

    # Find the audio stream with the highest bitrate
    highest_quality_stream = max(audio_streams, key=lambda x: x['bitrate'])

    # Get the itag of the highest quality stream
    itag = highest_quality_stream['itag']

    # Download the highest quality audio stream
    audio_stream = yt.streams.get_by_itag(itag)
    audio_stream.download(output_path=DOWNLOAD_FOLDER, filename='highest_quality_audio.mp3')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_audio(url)
    return send_from_directory(DOWNLOAD_FOLDER, 'highest_quality_audio.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
