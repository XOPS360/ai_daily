from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    dialogue: Optional[List[str]]
    next_speaker: Optional[str]
    members: Optional[List[str]]
    team_description: Optional[List[str]]