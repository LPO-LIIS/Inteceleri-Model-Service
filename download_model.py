import os
from huggingface_hub import snapshot_download
from dotenv import load_dotenv

load_dotenv()

model_dir = os.getenv("MODEL_DIR")
# Pegando o token de ambiente
HF_TOKEN = os.getenv("HF_TOKEN")

# Informações do modelo
REPO_ID = "LPO-UFPA/inteceleri-shapes"

# Faz o download apenas se o modelo ainda não existir
if not os.path.exists(os.path.join(model_dir, "preprocessor_config.json")):
    print("Downloading model...")
    os.makedirs(model_dir, exist_ok=True)
    snapshot_download(
        repo_id=REPO_ID,  # Nome do repositório
        local_dir=model_dir,  # Diretório onde os arquivos serão salvos
        token=HF_TOKEN,  # Token de autenticação (se necessário)
        repo_type="model",  # Tipo do repositório
        revision="main",  # Branch ou commit específico
        ignore_patterns=["*.md", "*.txt"],  # Ignora arquivos desnecessários
    )
    print("Model downloaded successfully!")
else:
    print("Model already exists, skipping download.")
