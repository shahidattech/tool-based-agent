from pydantic_settings import BaseSettings

class settings(BaseSettings):
    API_V1_STR: str = "llm/api/v1/assistant"
    PROJECT_NAME: str = "Finance Assistant"
    PROJECT_DESCRIPTION: str = "Finance Assistant is a service that provides financial information to the user."
    PROJECT_VERSION: str = "0.1.0"
    ALLOWED_HOSTS: list = ["*"]
    LOG_LEVEL: str = "debug"
    LOG_GROUP_NAME: str = "FinanceAssistant"
    LOG_STREAM_NAME: str = "FinanceAssistantStream"
    LOGGERS: list = ["console"]
    


settings = settings()