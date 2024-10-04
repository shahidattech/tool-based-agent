from pydantic_settings import BaseSettings

class settings(BaseSettings):
    API_V1_STR: str = "nova/ai-fi/api/v1/assistant"
    PROJECT_NAME: str = "Nova AI Finance Assistant"
    PROJECT_DESCRIPTION: str = "Nova AI Finance Assistant"
    PROJECT_VERSION: str = "0.1.0"
    ALLOWED_HOSTS: list = ["*"]
    LOG_LEVEL: str = "debug"
    LOG_GROUP_NAME: str = "NovaAIFinanceAssistant"
    LOG_STREAM_NAME: str = "NovaAIFinanceAssistantStream"
    LOGGERS: list = ["console"]
    


settings = settings()