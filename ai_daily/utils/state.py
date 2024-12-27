from operator import add
from typing import TypedDict, List, Optional, Annotated


class DailyState(TypedDict):
    dialogue: Annotated[List[str], add]
    complete_speakers: Annotated[List[str], add]
    next_speaker: Optional[str]
    facilitator: Optional[str]
