from ai_daily.utils.person_factory import read_persons, EmployeeBase
from ai_daily.utils.prompt import orkestrator_prompt
from ai_daily.utils.model import get_model
from pydantic import BaseModel
from typing import Literal


def get_route_model(options_names: list[str]):
    class Route(BaseModel):
        """Выбери следующую роль"""
        next: Literal[*options_names]
    return Route


def make_team_description(state):
    'Init Members'
    employees = {}
    persons = read_persons()
    for name, data in persons.items():
        employees[name] = EmployeeBase(**data)        
    state['team_description'] = [f'{person.name} -- {person.role}, который {person.duties}' for person in employees.values()]
    return state


def orkestrator(state):
    '''Orkestrator'''
    llm = get_model(model_name="openai")
    partial_client_choose_prompt = orkestrator_prompt.partial(
        options=str(state['members'])
    )
    route_model = get_route_model(state['members'] + ['End'])
    chain = partial_client_choose_prompt | llm.with_structured_output(route_model)
    state['next_speaker'] = chain.invoke({'dialogue': state['dialogue'],'team_description': state['team_description']}).next
    print(f'Дальше говорит {state["next_speaker"]}')
    return state


def choose_person(state):
    return state['next_speaker']


def end_of_chat(state):
    'End of chat'
    return state
