import asyncio

from psycopg_pool import AsyncConnectionPool
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from ai_daily.utils.state import AOCState
from ai_daily.utils.config_schema import ConfigSchema


def make_graph(checkpointer: BaseCheckpointSaver = None) -> CompiledStateGraph:
    """Создание компилированного графа"""

    base_builder = StateGraph(AOCState, ConfigSchema)

    pass

    graph = base_builder.compile(checkpointer=checkpointer)
    return graph


async def make_graph_async_postgresql(pool: AsyncConnectionPool, setup: bool = False) -> CompiledStateGraph:
    """Создание графа с асинхронным подключением к postgresql"""
    checkpointer = AsyncPostgresSaver(pool)
    if setup:
        await checkpointer.setup()

    return make_graph(checkpointer)


async def make_graph_memory() -> CompiledStateGraph:
    """Создание графа с асинхронным подключением к postgresql"""
    checkpointer = MemorySaver()
    return make_graph(checkpointer)

if __name__ == '__main__':
    asyncio.run(make_graph_memory())
