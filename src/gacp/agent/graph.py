from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from modules.perception.module import PerceptionModule
from modules.world_model.module import WorldModelModule
from modules.decision.module import DecisionModule
from modules.action.module import ActionModule
from modules.memory.module import MemoryModule
from modules.introspection.module import IntrospectionModule
from .state import AgentState

perception_instance = PerceptionModule()
world_model_instance = WorldModelModule()
decision_instance = DecisionModule()
action_instance = ActionModule()
memory_instance = MemoryModule()

def perception_node(state) -> AgentState: 
    return perception_instance.update_state(state)

def world_model_node(state) -> AgentState: 
    return world_model_instance.update_state(state)

def decision_node(state) -> AgentState: 
    return decision_instance.update_state(state)

def action_node(state) -> AgentState: 
    return action_instance.update_state(state)

def memory_node(state) -> AgentState: 
    return memory_instance.update_state(state)

def build_workflow() -> CompiledStateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node("perception", perception_node)
    workflow.add_node("world_model", world_model_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("action", action_node)
    workflow.add_node("memory", memory_node) 

    workflow.set_entry_point("perception")

    workflow.add_edge(START, "perception")
    workflow.add_edge("perception", "world_model")
    workflow.add_edge("world_model", "decision")
    workflow.add_edge("decision", "action")
    workflow.add_edge("action", END)

    def should_reflect(state: AgentState):
        # TODO: Implement this stub. Stub: Always return END, never reflect
        return END

    workflow.add_conditional_edges(
        "action",
        should_reflect,
        {END: END} # TODO: Implement this stub. Stub. Change along with should_reflect
    )

    graph = workflow.compile()

    # Visualization. 
    # TODO: use langsmith
    mermaid_code = graph.get_graph().draw_mermaid()
    with open("architecture_graph.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_code)

    return graph