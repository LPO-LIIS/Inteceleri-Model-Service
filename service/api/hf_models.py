import os
import torch
import tensorflow.lite as tflite
from fastapi import FastAPI
from dotenv import load_dotenv
from transformers import AutoModelForImageClassification, AutoImageProcessor

load_dotenv()
MODEL_DIR = os.getenv("MODEL_DIR")

# Lifespan para carregar e descarregar o modelo
async def lifespan(app: FastAPI):
    try:
        # Carrega o modelo e o feature extractor
        app.state.resnet_feature_extractor = AutoImageProcessor.from_pretrained(MODEL_DIR, use_fast=False)
        app.state.resnet_model = AutoModelForImageClassification.from_pretrained(MODEL_DIR)
        app.state.resnet_model.eval()

        app.state.logger.debug("Resnet50 model and resources loaded.")
    
    except Exception as e:
        app.state.logger.error(f"Error loading resnet50 model: {e}")

    try:
        # Carrega o modelo TFLite
        app.state.mobilenet_model = tflite.Interpreter(
            model_path=os.path.join(MODEL_DIR, "sparse_geometa_model_MobileNetV2_num_01_quantized.tflite")
        )
        app.state.mobilenet_model.allocate_tensors()

        app.state.logger.debug("MobilenetV2 model and resources loaded.")
    
    except Exception as e:
        app.state.logger.error(f"Error loading mobilenetv2 model: {e}")

    yield  # Mantém a API rodando até que seja encerrada

    # Executado quando a API é encerrada
    app.state.resnet_model = None
    app.state.resnet_feature_extractor = None
    app.state.mobilenet_model = None
    torch.cuda.empty_cache()  # Limpa memória da GPU se estiver usando CUDA
    app.state.logger.debug("Model and resources cleaned up.")
