from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send
from pytube import YouTube
from PIL import Image
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    response = process_message(msg)
    send(response, broadcast=True)

def process_message(msg):
    msg = msg.lower()
    if msg.startswith('http'):
        # Assume it's a YouTube URL for now
        return download_video(msg)
    elif msg == '1':
        return 'Você escolheu: Download de música ou vídeo. Por favor, envie o link do vídeo.'
    elif msg == '2':
        return 'Você escolheu: Converter imagem. Por favor, envie a imagem no formato base64.'
    elif msg == '3':
        return 'Você escolheu: Converter vídeo. Por favor, envie o vídeo.'
    else:
        return 'Bem-vindo! Qual serviço você deseja? Pressione 1 - para download de música ou vídeo, 2 para converter imagem, 3 para converter vídeo.'

def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        filename = stream.download(DOWNLOAD_FOLDER)
        basename = os.path.basename(filename)
        return f'Vídeo baixado com sucesso! [Clique aqui para baixar](/download/{basename})'
    except Exception as e:
        return f'Ocorreu um erro ao baixar o vídeo: {str(e)}'

if __name__ == '__main__':
    socketio.run(app, debug=True)
