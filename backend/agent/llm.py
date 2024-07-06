from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

from core.config import settings

model = LlamaCpp(
    model_path=settings.MODEL_PATH,
    temperature=0,
    n_ctx=settings.n_ctx,
    max_tokens=2000,
    top_p=1,
    repeat_penalty=settings.repeat_penalty,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
)
