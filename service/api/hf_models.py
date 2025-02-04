import os
import torch
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from transformers import AutoModelForImageClassification, AutoImageProcessor

load_dotenv()
MODEL_DIR = os.getenv("MODEL_DIR")

# Lifespan para carregar e descarregar o modelo
async def lifespan(app: FastAPI):
    try:
        # Carrega o modelo e o feature extractor
        app.state.feature_extractor = AutoImageProcessor.from_pretrained(MODEL_DIR, use_fast=False)
        app.state.model = AutoModelForImageClassification.from_pretrained(MODEL_DIR)
        app.state.model.eval()

        app.state.logger.debug("Model and resources loaded.")
    
    except Exception as e:
        app.state.logger.error(f"Error loading model: {e}")

    yield  # Mantém a API rodando até que seja encerrada

    # Executado quando a API é encerrada
    app.state.model = None
    app.state.feature_extractor = None
    torch.cuda.empty_cache()  # Limpa memória da GPU se estiver usando CUDA
    app.state.logger.debug("Model and resources cleaned up.")