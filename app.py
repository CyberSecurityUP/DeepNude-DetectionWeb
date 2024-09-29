import os
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
import threading

from detector import NudeDetector

app = Flask(__name__)

# Caminho para armazenar os arquivos carregados
UPLOAD_FOLDER = 'static/uploads/'
CENSORED_FOLDER = 'static/censored/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CENSORED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CENSORED_FOLDER'] = CENSORED_FOLDER

# Inicializa o detector de nudez
detector = NudeDetector()


# Função para deletar arquivos com mais de 5 minutos
def clean_old_files(folder, max_age_seconds=300):
    now = time.time()
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                print(f"Deleted: {file_path} (older than 5 minutes)")


# Função que roda em segundo plano para limpar arquivos periodicamente
def start_cleaner():
    while True:
        # Limpa as pastas de uploads e censored
        clean_old_files(UPLOAD_FOLDER)
        clean_old_files(CENSORED_FOLDER)
        # Espera 5 minutos antes de rodar de novo
        time.sleep(300)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    # Primeiro, verifica se um arquivo foi enviado
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        # Salva a imagem no diretório de uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Realiza a detecção de nudez
        detections = detector.detect(filepath)
        is_improper = False
        for detection in detections:
            if detection['improper']:
                is_improper = True
                # Gera a imagem censurada
                random_name = detector.generate_random_name()
                censored_path = os.path.join(app.config['CENSORED_FOLDER'], f"censored_{random_name}.jpg")
                detector.censor(filepath, out_path=censored_path)

                return render_template('result.html',
                                       image_path=url_for('static',
                                                          filename=f'censored/{os.path.basename(censored_path)}'),
                                       message="Inappropriate content detected.")

        # Se não encontrar conteúdo impróprio, mostra a imagem original
        if not is_improper:
            return render_template('result.html',
                                   image_path=url_for('static', filename=f'uploads/{os.path.basename(filepath)}'),
                                   message="No inappropriate content detected.")

    # Se não houver arquivo enviado, verifica se há uma URL fornecida
    elif 'url' in request.form and request.form['url'] != '':
        img_url = request.form['url']
        img_path = detector.download_image_from_url(img_url)
        if img_path:
            # Realiza a detecção de nudez
            detections = detector.detect(img_path)
            is_improper = False
            for detection in detections:
                if detection['improper']:
                    is_improper = True
                    # Gera a imagem censurada
                    random_name = detector.generate_random_name()
                    censored_path = os.path.join(app.config['CENSORED_FOLDER'], f"censored_{random_name}.jpg")
                    detector.censor(img_path, out_path=censored_path)

                    return render_template('result.html',
                                           image_path=url_for('static',
                                                              filename=f'censored/{os.path.basename(censored_path)}'),
                                           message="Inappropriate content detected.")

            # Se não encontrar conteúdo impróprio, mostra a imagem original
            if not is_improper:
                return render_template('result.html',
                                       image_path=url_for('static', filename=f'uploads/{os.path.basename(img_path)}'),
                                       message="No inappropriate content detected.")

    # Se nenhum arquivo ou URL foi fornecido
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Inicia o processo de limpeza em segundo plano
    cleaner_thread = threading.Thread(target=start_cleaner, daemon=True)
    cleaner_thread.start()

    # Roda o app Flask
    app.run(debug=True)
