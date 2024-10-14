from pydantic_settings import BaseSettings

class settings(BaseSettings):
    API_V1_STR: str = "mocked/api/v1/webservices"
    PROJECT_NAME: str = "Mocked Web Services"
    PROJECT_DESCRIPTION: str = "These APIs services are called by the LLM Agent as needed based on User interaction to complete the transaction."
    PROJECT_VERSION: str = "0.1.0"
    ALLOWED_HOSTS: list = ["*"]
    LOG_LEVEL: str = "debug"
    LOG_GROUP_NAME: str = "webservices-logs"
    LOG_STREAM_NAME: str = "webservices-logs"
    LOGGERS: list = ["console"]
    


settings = settings()