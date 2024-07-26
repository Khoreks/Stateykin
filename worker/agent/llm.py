import os
import requests

from langchain_community.llms import LlamaCpp
from langchain_community.chat_models import ChatOllama

from config import settings


def get_llm(type="ollama"):
    if not os.path.exists(settings.MODEL_PATH):
        response = requests.get(settings.MODEL_URL)
        if response.status_code == 200:
            with open(settings.MODEL_PATH, "wb") as file:
                file.write(response.content)

    if type == "ollama":
        model = ChatOllama(
            model="gemma-2-9b-it-Q8_0_L",
            temperature=0,
            base_url='http://host.docker.internal:11434'
        )
    elif type == "llamacpp":
        model = LlamaCpp(
            model_path=settings.MODEL_PATH,
            temperature=settings.temperature,
            n_ctx=settings.n_ctx,
            max_tokens=settings.max_tokens,
            top_p=settings.top_p,
            repeat_penalty=settings.repeat_penalty,
            n_threads=settings.n_threads,
            n_gpu_layers=settings.n_gpu_layers,
            verbose=True
        )
    else:
        return None
    return model
