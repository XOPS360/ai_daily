from logging import Logger
from functools import lru_cache

from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langchain_gigachat.chat_models.gigachat import GigaChat
from langchain_core.language_models.chat_models import BaseChatModel

from ai_daily.utils.logger import get_logger


@lru_cache(maxsize=4)
def get_model_by_name(model_name: str) -> BaseChatModel:
    if model_name == 'openai-omni':
        model = ChatOpenAI(
            temperature=1,
            request_timeout=90.0,
            model='gpt-4o'
        )
    elif model_name == 'giga-pro':
        model = GigaChat(
            model='GigaChat-Pro',
            temperature=1,
            top_p=1,
            timeout=90.0,
            verify_ssl_certs=False,
            profanity_check=False,
        )
    elif model_name == 'giga-max':
        model = GigaChat(
            model='GigaChat-Max',
            temperature=1,
            top_p=1,
            timeout=90.0,
            verify_ssl_certs=False,
            profanity_check=False,
        )
    else:
        raise ValueError(f'Модель с именем "{model_name}" не поддерживается')
    return model


def get_model_by_config(config: RunnableConfig) -> BaseChatModel:
    return get_model_by_name(config['configurable'].get('model', 'openai-omni'))


def get_logger_by_config(config: RunnableConfig) -> Logger:
    logger = config['configurable'].get('logger')
    if logger is None:
        logger = get_logger()
    return logger
