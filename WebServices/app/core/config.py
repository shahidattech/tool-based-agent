from pydantic_settings import BaseSettings

class settings(BaseSettings):
    API_V1_STR: str = "nova/ai-fi/api/v1/webservices"
    PROJECT_NAME: str = "Nova AI Finance Webservoces"
    PROJECT_DESCRIPTION: str = "Provide set of Web services for Nova AI Finance Assistant"
    PROJECT_VERSION: str = "0.1.0"
    ALLOWED_HOSTS: list = ["*"]
    LOG_LEVEL: str = "debug"
    LOG_GROUP_NAME: str = "novaaifi-logs"
    LOG_STREAM_NAME: str = "novaaifi-logs"
    LOGGERS: list = ["console"]
    


settings = settings()