import os
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Adiciona o diretório raiz do projeto ao PYTHONPATH (melhor configurar no ambiente)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.routes.router import routes
from api.database import lifespan
from config import DevelopmentConfig, TestingConfig, ProductionConfig


def create_api(config_name="production"):
    """
    Cria o objeto FastAPI e configura o ambiente e as rotas.
    """
    app = FastAPI(
        title="Template API",
        version="1.0",
        description="API de exemplo para sistemas com banco de dados MongoDB.",
        lifespan=lifespan,
    )

    # Configurações baseadas no ambiente
    configure_api(app, config_name)

    # Registrar as rotas
    for route in routes:
        app.include_router(route, prefix="")

    return app


def configure_api(app, config_name):
    """
    Configurações de acordo com o ambiente (produção, desenvolvimento, teste).
    """
    config_class = None

    if config_name == "development":
        config_class = DevelopmentConfig()
        # Adicionar o middleware CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Lista de origens permitidas
            allow_credentials=True,
            allow_methods=["*"],  # Permite todos os métodos HTTP
            allow_headers=["*"],  # Permite todos os headers
        )
        # Configuração básica do logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    elif config_name == "testing":
        config_class = TestingConfig()
        # Configuração básica do logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    elif config_name == "production":
        config_class = ProductionConfig()
        # Configuração básica do logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    else:
        raise ValueError(f"Configuração desconhecida: {config_name}")

    # Definindo as configurações no app.state
    app.state.config = config_class
