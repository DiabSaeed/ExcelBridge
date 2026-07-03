from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    HOST: str = ""
    TOKEN: str = ""
    
    
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    

def get_settings():
    return Settings() #type: ignore