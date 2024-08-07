from flask import Flask, request, render_template, send_file
from pytube import YouTube
import yt_dlp
from moviepy.editor import AudioFileClip
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_conversor():
    youtube_url = request.form['url']
    output_path = 'output_audio.wav'
    download_path = 'downloaded_audio'

    # Baixar o vídeo do YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': download_path + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Procurar o arquivo baixado
    for file in os.listdir('.'):
        if file.startswith(download_path):
            download_path = file
            break

    # Converter o áudio para WAV
    audio_clip = AudioFileClip(download_path)
    audio_clip.write_audiofile(output_path, codec='pcm_s16le')

    # Fechar o clip para liberar recursos
    audio_clip.close()

    # Remover o arquivo de áudio baixado
    os.remove(download_path)

    return send_file(output_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)