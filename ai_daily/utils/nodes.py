import random

from langchain_core.prompts import ChatPromptTemplate

from ai_daily.utils.state import DailyState
from ai_daily.utils.config_schema import ConfigSchema
from langchain_core.runnables.base import RunnableLike
from ai_daily.utils.models import get_daily_speech_model, Employee
from ai_daily.utils.prompts import base_prompt, facilitator_start_prompt, facilitator_end_prompt
from ai_daily.utils.utils import (
    get_model_by_config,
    get_logger_by_config,
    get_all_speaker_full_names,
    get_daily_data_by_full_name,
    get_employee_by_full_name,
    tts,
    ttv,
)


def person_node_factory(person: Employee, prompt: ChatPromptTemplate = base_prompt) -> RunnableLike:
    personal_prompt = prompt.partial(
        person_info=person.prompt_representation(),
        dayli_info=get_daily_data_by_full_name(person.full_name)
    )

    def person_node(state: DailyState, config: ConfigSchema):
        logger = get_logger_by_config(config)
        logger.debug(f'Вход узла говорящего {person.node_name}')

        complete_speakers = state.get('complete_speakers', [])
        all_speakers = get_all_speaker_full_names()
        available_speakers = list(set(all_speakers) - set(complete_speakers))
        logger.debug(f'Доступные для выбора участники для разговора: {available_speakers}')

        llm = get_model_by_config(config)
        speech_model = get_daily_speech_model(available_speakers)
        chain = personal_prompt | llm.with_structured_output(speech_model)
        speech = chain.invoke(
            {
                'dialogue': state.get('dialogue'),
                'available_speakers': available_speakers,
            }
        )

        dialogue_speech = speech.speech
        if config['configurable'].get('video', False):
            ttv(dialogue_speech, person.full_name)
        elif config['configurable'].get('audio', False):
            tts(dialogue_speech, person.full_name)

        if not dialogue_speech.startswith(person.full_name):
            dialogue_speech = f'{person.full_name}: {speech.speech}'
        return {
            'dialogue': [dialogue_speech],
            'next_speaker': speech.next_speaker,
            'complete_speakers': [person.full_name]
        }

    person_node.__name__ = person.node_name
    return person_node


def jazz(state: DailyState, config: ConfigSchema):
    pass


jazz.__name__ = 'Jazz 📸'


def choose_facilitator(state: DailyState, config: ConfigSchema):
    logger = get_logger_by_config(config)
    logger.debug(f'Вход узла выбора фасилитатора встречи')
    facilitator = state.get('facilitator')
    facilitator_full_name = random.choice(get_all_speaker_full_names()) if facilitator is None else facilitator
    logger.debug(f'Фасилитатором выбран {facilitator_full_name}')
    return {'facilitator': facilitator_full_name}


choose_facilitator.__name__ = 'Выбор ведущего 🎤'


def facilitator_start(state: DailyState, config: ConfigSchema):
    logger = get_logger_by_config(config)
    logger.debug(f'Вход узла начало диалога от фасилитатора')

    available_speakers = get_all_speaker_full_names()
    logger.debug(f'Доступные для выбора участники для разговора: {available_speakers}')

    llm = get_model_by_config(config)
    speech_model = get_daily_speech_model(available_speakers)
    chain = facilitator_start_prompt | llm.with_structured_output(speech_model)

    facilitator_full_name = state['facilitator']
    person_info = get_employee_by_full_name(facilitator_full_name)
    speech = chain.invoke(
        {
            'person_info': person_info,
            'available_speakers': available_speakers,
        }
    )

    dialogue_speech = speech.speech
    if config['configurable'].get('video', False):
        ttv(dialogue_speech, facilitator_full_name)
    elif config['configurable'].get('audio', False):
        tts(dialogue_speech, facilitator_full_name)

    if not dialogue_speech.startswith(facilitator_full_name):
        dialogue_speech = f'{facilitator_full_name}: {speech.speech}'
    return {'dialogue': [dialogue_speech], 'next_speaker': speech.next_speaker}


facilitator_start.__name__ = 'Начало дейли 🚀'


def facilitator_end(state: DailyState, config: ConfigSchema):
    logger = get_logger_by_config(config)
    logger.debug(f'Вход узла начало диалога от фасилитатора')

    available_speakers = get_all_speaker_full_names()
    logger.debug(f'Доступные для выбора участники для разговора: {available_speakers}')

    llm = get_model_by_config(config)
    chain = facilitator_end_prompt | llm

    facilitator_full_name = state['facilitator']
    person_info = get_employee_by_full_name(facilitator_full_name)
    speech = chain.invoke(
        {
            'dialogue': state.get('dialogue'),
            'person_info': person_info,
            'available_speakers': available_speakers,
        }
    )

    dialogue_speech = speech.content
    if config['configurable'].get('video', False):
        ttv(dialogue_speech, facilitator_full_name)
    elif config['configurable'].get('audio', False):
        tts(dialogue_speech, facilitator_full_name)

    if not dialogue_speech.startswith(facilitator_full_name):
        dialogue_speech = f'{facilitator_full_name}: {speech.content}'
    return {'dialogue': [dialogue_speech], 'next_speaker': None}


facilitator_end.__name__ = 'Окончание дейли 🏁'


def next_speaker(state: DailyState, config: ConfigSchema):
    return state['next_speaker'] if state['next_speaker'] is not None else 'Все поговорили'
