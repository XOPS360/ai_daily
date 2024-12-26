from typing import Literal, Optional, TypedDict


class ConfigSchema(TypedDict):
    """Схема конфигурации"""

    model: Optional[Literal['openai-omni', 'giga-pro', 'giga-max']]
