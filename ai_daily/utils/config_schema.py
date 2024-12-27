from typing import Literal, Optional, TypedDict


class ConfigSchema(TypedDict):
    """Схема конфигурации"""
    model: Literal['openai-omni', 'giga-pro', 'giga-max']
    audio: bool
    video: bool
