import json
import subprocess
from pathlib import Path
from logging import Logger
from functools import lru_cache

import pyttsx3
from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langchain_gigachat.chat_models.gigachat import GigaChat
from langchain_core.language_models.chat_models import BaseChatModel

from ai_daily.utils.logger import get_logger
from ai_daily.utils.constants import TEAM_DATA_PATH, DAILY_DATA_PATH
from ai_daily.utils.models import Employee, PersonDayInfo


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


@lru_cache(maxsize=1)
def get_team_data(path: Path = TEAM_DATA_PATH) -> list[Employee]:
    return [Employee(**employee) for employee in json.loads(path.read_text())]


@lru_cache(maxsize=1)
def get_all_full_names() -> list[str]:
    return [employee.full_name for employee in get_team_data()]


@lru_cache(maxsize=1)
def get_all_speaker_full_names() -> list[str]:
    return [daily_data.full_name for daily_data in get_daily_data()]


@lru_cache(maxsize=20)
def get_daily_data_by_full_name(full_name: str) -> PersonDayInfo:
    for daily_data in get_daily_data():
        if daily_data.full_name == full_name:
            return daily_data
    raise ValueError(f'{full_name} нет в списке на день')


@lru_cache(maxsize=20)
def get_employee_by_full_name(full_name: str) -> Employee:
    for employee in get_team_data():
        if employee.full_name == full_name:
            return employee
    raise ValueError(f'{full_name} нет в списке на день')


@lru_cache(maxsize=1)
def get_daily_data(path: Path = DAILY_DATA_PATH) -> list[PersonDayInfo]:
    return [PersonDayInfo(**day_info) for day_info in json.loads(path.read_text())]


@lru_cache(maxsize=1)
def get_audio_engine() -> pyttsx3.Engine:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'ru')  # Выбираем русский голос
    return engine


def tts(text: str, person_name: str):
    # engine = get_audio_engine()
    # engine.say(text)
    # engine.runAndWait()
    def tts(text: str, person_name: str):

        speaker_wav = "Audio/" + person_name.replace(" ", "") + ".wav"
        file_path = "Audio/" + person_name.replace(" ", "") + "_gen.wav"
        python_executable = r"..\TTS\TTS\venv\Scripts\python.exe"
        script_path = r"..\TTS\TTS\voice.py"

        command = [
            python_executable,
            script_path,
            "--text", text,
            "--speaker_wav", speaker_wav,
            "--file_path", file_path
        ]

        # Запускаем команду
        try:
            subprocess.run(command, check=True)
            print("Команда выполнена успешно!")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка выполнения команды: {e}")

        # engine = get_audio_engine()
        # engine.say(text)
        # engine.runAndWait()

        target_directory = r"..\Lipsing\Wav2lip"
        command = (
                r"..\venv\Scripts\python.exe inference.py " +
                r"--checkpoint_path checkpoints\wav2lip.pth --face ../../ai_daily_main/Video/"
                + person_name.replace(" ", "") +
                r".mp4 " + r"--audio ../../ai_daily_main/Audio/"
                + person_name.replace(" ","") +
                r"_gen.wav " + r"--pads 0 0 10 0 --resize_factor 1 --nosmooth --outfile ../../ai_daily_main/Video/"
                + person_name.replace(" ", "") + r"_gen.mp4" + r"--static 1"
        )

        try:
            subprocess.run(command, cwd=target_directory, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e}")

def ttv(text: str, person_name: str):
    pass
