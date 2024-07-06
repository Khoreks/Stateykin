import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Project
    PROJECT_NAME: str = "Stateykin"
    PROJECT_VERSION: str = "0.1.0"

    # ML
    MODEL_PATH: str = os.getenv("MODEL_PATH")
    MODEL_URL: str = os.getenv("MODEL_URL")
    MODEL_TYPE: str = os.getenv("MODEL_TYPE")
    FIRST_MESSAGE: str = os.getenv("FIRST_MESSAGE")
    # QASUPPORT_PROMPT: str = os.getenv("QASUPPORT_PROMPT")
    # WEBSUPPORT_PROMPT: str = os.getenv("WEBSUPPORT_PROMPT")
    n_ctx: int = int(os.getenv("n_ctx"))
    n_parts: int = int(os.getenv("n_parts"))
    top_k: int = int(os.getenv("top_k"))
    top_p: float = float(os.getenv("top_p"))
    temperature: float = float(os.getenv("temperature"))
    repeat_penalty: float = float(os.getenv("repeat_penalty"))

    web_max_results: int = os.getenv("web_max_results")

settings = Settings()
