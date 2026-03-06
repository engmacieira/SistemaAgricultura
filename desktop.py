import webview
import threading
import uvicorn
import time
import urllib.request

# Importa o nosso app FastAPI (que já inicializa o seu setup_logging() internamente)
from app.main import app

PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"

def run_server():
    # Retornamos o log_level para "info" para que o seu logging_config.py capture tudo
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", log_config=None)

if __name__ == '__main__':
    print("Iniciando o servidor em background. Aguarde...")
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    server_ready = False
    for _ in range(50):
        try:
            urllib.request.urlopen(URL)
            server_ready = True
            break
        except Exception:
            time.sleep(0.1)

    if not server_ready:
        print("❌ Erro fatal: O servidor demorou muito para iniciar.")
    else:
        print("✅ Servidor Online! Abrindo interface gráfica...")
        
        webview.create_window(
            title="Sistema de Agricultura",
            url=URL,
            width=1280,
            height=720,
            min_size=(800, 600)
        )
        
        webview.start(private_mode=True)