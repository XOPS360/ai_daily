from langgraph.graph import StateGraph, END
from ai_daily.utils.state import AgentState
from ai_daily.utils.person_factory import make_persons
from ai_daily.utils.nodes import (
    choose_person,
    orkestrator,
    make_team_description,
    end_of_chat
)


members = make_persons()
graph_builder = StateGraph(AgentState)

graph_builder.add_node(end_of_chat.__doc__, end_of_chat)
graph_builder.add_node(make_team_description.__doc__, make_team_description)
graph_builder.add_node(orkestrator.__doc__, orkestrator)

graph_builder.add_edge(make_team_description.__doc__, orkestrator.__doc__)

for_cond = {'End': end_of_chat.__doc__}
for name, class_ in members.items():
    graph_builder.add_node(name, class_.talker)
    graph_builder.add_edge(name, orkestrator.__doc__)
    for_cond[name] = name

graph_builder.add_conditional_edges(
    orkestrator.__doc__,
    choose_person,
    for_cond,
)

graph_builder.set_entry_point(make_team_description.__doc__)
graph_builder.set_finish_point(end_of_chat.__doc__)

graph = graph_builder.compile()
