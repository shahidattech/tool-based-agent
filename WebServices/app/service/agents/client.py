
import os
import abc

#openai client
from openai import OpenAI, types

openai_api_key = os.getenv('OPENAI_API_KEY', '')

class ClientBase(abc.ABC):
  @abc.abstractmethod
  def generate_answer():
    pass

class OpenaiClient(ClientBase):
  def __init__(self, api_key: str=openai_api_key):
    self.client = OpenAI(
        api_key=api_key
    )
  def generate_answer(self, messages: list, **kwargs)->str:
    # logger.debug(f"================== messages = {messages}")
    response = self.client.chat.completions.create(
              model=kwargs.get('model') if 'model' in kwargs else "gpt-4",
              messages=messages,
              tools=kwargs.get('tools') if 'tools' in kwargs else [],
              )
    return response

def ClientFactory(platform ="openai"):
    client = {
        "openai": OpenaiClient,
    }
    return client[platform]()