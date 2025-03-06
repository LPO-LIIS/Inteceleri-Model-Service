import uvicorn

# Configurações do Uvicorn
uvicorn_config = {
    "app": "service.api:create_api",     # Aplicação
    "host": "0.0.0.0",       # Escutar em todas as interfaces de rede
    "port": 8000,            # Porta padrão
    "workers": 4,            # Número de workers
    "log_level": "info",     # Nível de log
    "timeout_keep_alive": 30, # Tempo para manter conexões HTTP abertas
    "access_log": True,      # Habilitar logs de acesso
    "factory": True,         # Usar factory para criar a aplicação
}

if __name__ == "__main__":
    uvicorn.run(**uvicorn_config)
