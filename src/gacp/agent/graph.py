from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from modules.perception.module import PerceptionModule
from modules.world_model.module import WorldModelModule
from modules.decision.module import DecisionModule
from modules.action.module import ActionModule
from modules.memory.module import MemoryModule
from modules.introspection.module import IntrospectionModule
from .state import AgentState


class Graph:

    def build_workflow(self) -> CompiledStateGraph:
        workflow = StateGraph(AgentState)

        workflow.add_node("perception", self._perception_node)
        workflow.add_node("world_model", self._world_model_node)
        workflow.add_node("decision", self._decision_node)
        workflow.add_node("action", self._action_node)
        workflow.add_node("memory", self._memory_node) 

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

    def _perception_node(self, state) -> AgentState: 
        perception_instance = PerceptionModule()
        return perception_instance.update_state(state)

    def _world_model_node(self, state) -> AgentState: 
        world_model_instance = WorldModelModule()
        return world_model_instance.update_state(state)

    def _decision_node(self, state) -> AgentState: 
        decision_instance = DecisionModule()
        return decision_instance.update_state(state)

    def _action_node(self, state) -> AgentState: 
        action_instance = ActionModule()
        return action_instance.update_state(state)

    def _memory_node(self, state) -> AgentState: 
        memory_instance = MemoryModule()
        return memory_instance.update_state(state)
