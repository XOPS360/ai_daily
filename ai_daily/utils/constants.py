import os
import logging
from pathlib import Path

# Константы путей
UTILS_PATH = Path(__file__).parent.resolve()
PROJECT_PATH = UTILS_PATH.parent
DATA_PATH = PROJECT_PATH / 'data'
TEAM_DATA_PATH = DATA_PATH / 'team.json'
DAILY_DATA_PATH = DATA_PATH / 'daily.json'

LOGGER_NAME = 'ai_daily'
LOGGER_LEVEL = logging.DEBUG if 'GRAPH_DEBUG' in os.environ else logging.INFO
LOGGER_DIRPATH = PROJECT_PATH / 'logs'
LOGGER_FILEPATH = LOGGER_DIRPATH / f'{LOGGER_NAME}.log'

DEFAULT_ATTEMPT_COUNT = 5
DEFAULT_TIMEOUT_EXEC_CODE = 120
