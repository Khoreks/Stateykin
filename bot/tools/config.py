import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Project
    PROJECT_NAME: str = "Stateykin"
    PROJECT_VERSION: str = "1.0.0"

    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # Messages
    start_message: str = os.getenv("start_message")
    help_message: str = os.getenv("help_message")
    new_post_message: str = os.getenv("new_post_message")
    low_info_message: str = os.getenv("low_info_message")
    server_error_message: str = os.getenv("server_error_message")
    thumbs_up_message: str = os.getenv("thumbs_up_message")
    neutrality_message: str = os.getenv("neutrality_message")
    thumbs_down_message: str = os.getenv("thumbs_down_message")
    start_generate_message: str = os.getenv("start_generate_message")
    bot_detect_message: str = os.getenv("bot_detect_message")

    # Backend
    BACKEND_PROTOCOL: str = os.getenv("BACKEND_PROTOCOL")
    BACKEND_HOST: str = os.getenv("BACKEND_HOST")
    BACKEND_PORT: str = os.getenv("BACKEND_PORT")
    BACKEND_URL: str = BACKEND_PROTOCOL + "://" + BACKEND_HOST + ":" + BACKEND_PORT


settings = Settings()
