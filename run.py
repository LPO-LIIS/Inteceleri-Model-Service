import os
import uvicorn
from service.api import create_api
from dotenv import load_dotenv

load_dotenv()

from download_model import get_resnet3d_model

get_resnet3d_model(os.getenv("MODEL_DIR"))
template_api = create_api(config_name="development")

if __name__ == "__main__":
    uvicorn.run(template_api, port=8000)
