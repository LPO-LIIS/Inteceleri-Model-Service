import uvicorn
from service.api import create_api

template_api = create_api(config_name="development")

if __name__ == "__main__":
    uvicorn.run(template_api, port=8000)
