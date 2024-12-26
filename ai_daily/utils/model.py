from functools import lru_cache
from langchain_openai import ChatOpenAI


@lru_cache(maxsize=1)
def get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=1, model_name="gpt-4o")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")
    return model
