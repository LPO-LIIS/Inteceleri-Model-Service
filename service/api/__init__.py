import os
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Adiciona o diretório raiz do projeto ao PYTHONPATH (melhor configurar no ambiente)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.routes.router import routes
from api.hf_models import lifespan
from config import DevelopmentConfig, TestingConfig, ProductionConfig


def create_api(config_name="production"):
    """
    Cria o objeto FastAPI e configura o ambiente e as rotas.
    """
    app = FastAPI(
        title="API de Inferência para Modelos de Reconhecimento de Formas Geométricas",
        version="1.1",
        description=(
            "Esta API fornece inferência de modelos treinados para **reconhecimento de formas geométricas** "
            "tanto **Tridimensionais (3D)** quanto **Bidimensionais (2D)**. "
            "Desenvolvida pela **Inteceleri** e pelo **LPO**, ela permite o envio de imagens para **classificação**, "
            "utilizando redes neurais profundas baseadas em ResNet-50 e outros modelos treinados. \n\n"
            
            "🔹 **Principais Funcionalidades:**\n"
            "✔️ **Classificação de Formas Geométricas 3D** (cilindro, cone, esfera, paralelepípedo, etc.)\n"
            "✔️ **Classificação de Formas Geométricas 2D** (círculo, quadrado, triângulo, retângulo, etc.)\n"
            "✔️ Suporte a **upload de imagens** para inferência\n"
            "✔️ Modelos otimizados para **alta precisão e desempenho**\n\n"

            "📌 **Tecnologias Utilizadas:**\n"
            "- 🖥️ **FastAPI** para criação da API\n"
            "- 🧠 **Hugging Face Transformers** para carregamento do modelo\n"
            "- 🔥 **PyTorch** para inferência de deep learning\n\n"

            "📝 **Como Usar:**\n"
            "1️⃣ Faça o upload de uma imagem contendo uma **forma geométrica** para a rota específica.\n"
            "2️⃣ A API processará a imagem e retornará a **classe predita**.\n"
            "3️⃣ Utilize os endpoints `/resnet3d` para modelos 3D e `EM BREVE` para modelos 2D.\n\n"

            "📍 **Exemplo de Entrada:**\n"
            "Envie um arquivo de imagem no formato **JPEG ou PNG** via requisição `POST`.\n\n"
            
            "📤 **Exemplo de Resposta:**\n"
            "```json\n"
            "{\n"
            "    \"prediction\": \"Esfera\"\n"
            "}\n"
            "```\n"
        ),
        lifespan=lifespan,
        root_path="/inteceleri/models/api/" # URL Path: https://services.liis.com.br{path}
    )

    # Configurações baseadas no ambiente
    configure_api(app, config_name)

    # Registrar as rotas
    for route in routes:
        app.include_router(route, prefix="")

    app.state.logger.debug(f"Rotas registradas")

    return app


def configure_api(app, config_name):
    """
    Configurações de acordo com o ambiente (produção, desenvolvimento, teste).
    """
    config_class = None
    log_level = logging.INFO  # Padrão para produção

    if config_name == "development":
        config_class = DevelopmentConfig()
        log_level = logging.DEBUG  # Mais verboso no ambiente de desenvolvimento
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Lista de origens permitidas
            allow_credentials=True,
            allow_methods=["*"],  # Permite todos os métodos HTTP
            allow_headers=["*"],  # Permite todos os headers
        )

    elif config_name == "testing":
        config_class = TestingConfig()
        log_level = logging.DEBUG

    elif config_name == "production":
        config_class = ProductionConfig()
        log_level = logging.INFO

    else:
        raise ValueError(f"Configuração desconhecida: {config_name}")

    # Definindo as configurações no app.state
    app.state.config = config_class

    # Configuração correta do logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]  # Envia logs para stdout
    )

    # Criar logger principal da API e armazenar em `app.state`
    app.state.logger = logging.getLogger("api")
    app.state.logger.setLevel(log_level)
    app.state.logger.info(f"API iniciada no ambiente: {config_name}")
