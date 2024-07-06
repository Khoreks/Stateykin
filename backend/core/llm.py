import os
from llama_cpp import Llama
import requests
from core.config import settings


class LLM:
    def __init__(self):
        self.name = settings.MODEL_PATH.split("/")[-1]
        self.model_path = settings.MODEL_PATH

    @staticmethod
    def download_model():
        response = requests.get(settings.MODEL_URL)
        if response.status_code == 200:
            with open(settings.MODEL_PATH, "wb") as file:
                file.write(response.content)


class LLAMA(LLM):
    def __init__(self):
        super().__init__()
        self.model = None

    def load_model(self):
        if not os.path.exists(self.model_path):
            self.download_model()
        self.model = Llama(
            model_path=settings.MODEL_PATH,
            n_ctx=settings.n_ctx,
            n_parts=settings.n_parts,
            n_threads=6,
            n_gpu_layers=33,
            verbose=True
        )

    @staticmethod
    def chat_format(dialogue: list[[str, str]]):
        return [{"role": role, "content": message} for role, message in dialogue]

    def generate(self,
                 messages,
                 temperature=settings.temperature,
                 top_k=settings.top_k,
                 top_p=settings.top_p,
                 repeat_penalty=settings.repeat_penalty,
                 stream=True,
                 ):
        response = self.model.create_chat_completion(
            messages,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
        )
        response_content = response['choices'][0]['message']
        return response_content
