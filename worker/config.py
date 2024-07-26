import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Project
    PROJECT_NAME: str = "Assistant"
    PROJECT_VERSION: str = "0.3.0"

    # ML
    MODEL_PATH: str = os.getenv("MODEL_PATH")
    MODEL_URL: str = os.getenv("MODEL_URL")
    MODEL_TYPE: str = os.getenv("MODEL_TYPE")
    n_ctx: int = int(os.getenv("n_ctx"))
    max_tokens: int = int(os.getenv("max_tokens"))
    top_k: int = int(os.getenv("top_k"))
    top_p: float = float(os.getenv("top_p"))
    temperature: float = float(os.getenv("temperature"))
    repeat_penalty: float = float(os.getenv("repeat_penalty"))
    n_threads: int = int(os.getenv("n_threads"))
    n_gpu_layers: int = int(os.getenv("n_gpu_layers"))

    # Rabbitmq
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT: str = int(os.getenv("RABBITMQ_PORT"))
    RABBITMQ_VIRTUAL_HOST: str = os.getenv("RABBITMQ_VIRTUAL_HOST")
    RABBITMQ_USERNAME: str = os.getenv("RABBITMQ_USERNAME")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD")

    # Search
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID")
    web_max_results: int = os.getenv("web_max_results")

    # Chunk
    chunk_size: int = int(os.getenv("chunk_size"))
    chunk_overlap: int = int(os.getenv("chunk_overlap"))
    chunk_max_words: int = int(os.getenv("chunk_max_words"))


settings = Settings()
