import os


class ConfigSettings(object):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    AZURE_API_KEY: str = os.getenv("AZURE_API_KEY", "")
    AZURE_API_BASE: str = os.getenv("AZURE_API_BASE", "")
    AZURE_API_VERSION: str = os.getenv("AZURE_API_VERSION", "")
    AZURE_DEPLOYMENT_NAME: str = os.getenv("AZURE_DEPLOYMENT_NAME", "")


settings = ConfigSettings()
