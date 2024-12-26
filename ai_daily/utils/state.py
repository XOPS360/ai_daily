from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage

class AIDailyState(TypedDict):
    messages: list[AnyMessage]
    done_tasks: list[str]
    today_tasks: list[str]
    comment: str
