from pydantic import BaseSettings

class Config(BaseSettings):
  OPENAI_API_KEY: str
  OPENAI_CHAT_MAX_TOKEN: int
  
  class Config:
    env_file = "./.env"

config = Config()