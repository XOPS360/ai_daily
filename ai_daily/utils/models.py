import json
from typing import List, Literal
from pydantic import TypeAdapter

from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr


class Phone(BaseModel):
    mobile: Optional[constr(pattern=r'^\+7 \d{3} \d{3}-\d{2}-\d{2}$')] = None
    work: Optional[constr(pattern=r'^8-\d{8}$')] = None

    def __str__(self):
        phone_info = ''
        if self.mobile is not None:
            phone_info += f'Мобильный телефон: {self.mobile}\n'
        if self.mobile is not None:
            phone_info += f'Рабочий телефон: {self.work}\n'
        return phone_info


class Email(BaseModel):
    sigma: EmailStr
    alpha: EmailStr

    def __str__(self):
        return (
            f'Почта SIGMA: {self.sigma}'
            f'Почта ALPHA: {self.alpha}'
        )


class Employee(BaseModel):
    full_name: str
    name: str
    node_name: Optional[str] = None
    role: str
    employee_number: constr(pattern=r'^\d+$')
    position: str
    hr_role: str
    linear_structure: str
    team_role: str
    phone: Optional[Phone] = None
    email: Email
    personality: str
    duties: str

    def __str__(self):
        return f'Сотрудник {self.full_name} ({self.role}) - {self.personality}'

    def prompt_representation(self) -> str:
        return (
            f'Имя: {self.name} ({self.full_name})'
            f'Роль: {self.role}'
            f'Описание: {self.personality}'
            f'Обязанности: {self.duties}'
        )


class PersonDayInfo(BaseModel):
    full_name: str
    completed_tasks: List[str]
    plans_for_today: List[str]
    questions: List[str]

    def __str__(self):
        completed = "\n  ".join(self.completed_tasks)
        plans = "\n  ".join(self.plans_for_today)
        return (
            f"Выполненные задачи:\n  {completed}\n"
            f"Планы на сегодня:\n  {plans}"
        )

    def prompt_representation(self) -> str:
        return self.__str__()


def get_daily_speech_model(options_speaker_names: list[str]):
    if len(options_speaker_names) == 0:
        next_speaker_type = str
    else:
        next_speaker_type = Literal[*options_speaker_names]
    class DailySpeech(BaseModel):
        """Информация речи для встречи дейли"""
        speech: str = Field(description='Речь для встречи дейли')
        next_speaker: Optional[next_speaker_type] = Field(
            description='Полное имя человека, кому передается слово. Выбирается случайно из списка. '
                        f'Если список пуст, то не выбирай никого. Здесь обязательно полное имя человека. '
                        f'Выбери из списка: {options_speaker_names}'
        )
    return DailySpeech
