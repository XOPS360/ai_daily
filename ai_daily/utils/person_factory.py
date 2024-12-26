import os
import json
from pydantic import BaseModel
from ai_daily.utils.model import get_model
from ai_daily.utils.prompt import person_prompt


class EmployeeBase(BaseModel):
    name: str
    role: str
    time_in_team: str
    personality: str
    duties: str
    completed_tasks: str
    plans_for_today: str

    def talker(self, state):
        print(f'{self.__doc__} говорит:\n')
        llm = get_model(model_name="openai")
        descr = {k: v for k, v in self.__dict__.items() if not k.startswith('__')}
        partial_client_choose_prompt = person_prompt.partial(**descr)
        B = partial_client_choose_prompt | llm
        answ = B.invoke({'dialogue': state['dialogue'],
                         'team_description': state['team_description']})
        print(f"({self.__doc__}){answ.content}")
        state['dialogue'].append(f"({self.__doc__}) {answ.content}")
        return state
    

def read_persons():
    with open(os.path.join('ai_daily', 'utils', 'data', 'Persons.json'), 'r', encoding="utf-8") as file:
        persons = json.load(file)
    
    return persons


def make_persons():
    employees = {}
    persons = read_persons()
    for name, data in persons.items():
        employees[name] = EmployeeBase(**data)
    for name, class_ in employees.items():
        class_.__doc__ = name
    return employees
