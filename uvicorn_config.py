import uvicorn
from service.api import create_api

# Configuração do ambiente
config_name = "production"

# Criar a aplicação com base na configuração
template_api = create_api(config_name=config_name)

# Configurações do Uvicorn
uvicorn_config = {
    "app": template_api,     # Aplicação
    "host": "0.0.0.0",       # Escutar em todas as interfaces de rede
    "port": 8000,            # Porta padrão
    "workers": 3,            # Número de workers
    "log_level": "info",     # Nível de log
    "timeout_keep_alive": 30, # Tempo para manter conexões HTTP abertas
    "access_log": True,      # Habilitar logs de acesso
}

if __name__ == "__main__":
    uvicorn.run(**uvicorn_config)
