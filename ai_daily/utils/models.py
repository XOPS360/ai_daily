from pydantic import BaseModel, Field


class SpeakerData(BaseModel):
    name: str = Field(description='Имя')
    role: str = Field(description='Роль')
    character: str = Field(description='Характер')
    workload: str = Field(description='Чем занимается на работе')
