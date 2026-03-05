import webview
import threading
import uvicorn
import time
import urllib.request

# Importa o nosso app FastAPI
from app.main import app

PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"

def run_server():
    # Roda o servidor FastAPI (silencioso para não poluir o terminal do .exe depois)
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")

if __name__ == '__main__':
    print("Iniciando o servidor em background. Aguarde...")
    
    # 1. Inicia o Backend em uma Thread (tarefa em paralelo)
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 2. Aguarda o servidor acordar (para evitar que a janela abra em branco)
    server_ready = False
    for _ in range(50):
        try:
            # Tenta dar um "ping" na raiz. Se responder, o servidor subiu.
            urllib.request.urlopen(URL)
            server_ready = True
            break
        except Exception:
            time.sleep(0.1)

    if not server_ready:
        print("Erro: O servidor demorou muito para iniciar.")
    else:
        print("Servidor Online! Abrindo interface gráfica...")
        
        # 3. Cria a Janela Nativa do Sistema Operacional
        webview.create_window(
            title="Sistema de Agricultura",
            url=URL,
            width=1280,   # Largura inicial
            height=720,   # Altura inicial
            min_size=(800, 600) # Evita que o usuário esprema muito a tela
        )
        
        # 4. Inicia o loop da interface (A partir daqui o app fica aberto)
        # O parâmetro private_mode=False permite que o LocalStorage (seu token de login) funcione!
        webview.start(private_mode=False)