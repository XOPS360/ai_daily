from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver

from ai_daily.utils.state import DailyState
from ai_daily.utils.utils import get_all_speaker_full_names, get_employee_by_full_name
from ai_daily.utils.nodes import (
    person_node_factory,
    jazz,
    choose_facilitator,
    facilitator_start,
    facilitator_end,
    next_speaker,
)


def make_graph(checkpointer: BaseCheckpointSaver = None) -> CompiledStateGraph:
    graph_builder = StateGraph(DailyState)

    graph_builder.add_node(jazz.__name__, jazz)
    graph_builder.add_node(choose_facilitator.__name__, choose_facilitator)
    graph_builder.add_node(facilitator_start.__name__, facilitator_start)
    graph_builder.add_node(facilitator_end.__name__, facilitator_end)

    graph_builder.add_edge(choose_facilitator.__name__, facilitator_start.__name__)
    graph_builder.add_edge(facilitator_start.__name__, jazz.__name__)

    team_nodes_map = {'Все поговорили': facilitator_end.__name__}
    for speaker_full_name in get_all_speaker_full_names():
        person = get_employee_by_full_name(speaker_full_name)
        person_node = person_node_factory(person)
        graph_builder.add_node(person_node.__name__, person_node)
        graph_builder.add_edge(person_node.__name__, jazz.__name__)
        team_nodes_map[person.full_name] = person_node.__name__

    graph_builder.add_conditional_edges(
        jazz.__name__,
        next_speaker,
        team_nodes_map
    )

    graph_builder.set_entry_point(choose_facilitator.__name__)
    graph_builder.set_finish_point(facilitator_end.__name__)

    graph = graph_builder.compile(checkpointer=checkpointer)
    return graph


def make_graph_memory() -> CompiledStateGraph:
    """Создание графа с асинхронным подключением к postgresql"""
    checkpointer = MemorySaver()
    return make_graph(checkpointer)