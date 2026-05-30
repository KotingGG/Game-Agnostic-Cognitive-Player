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

        # Adding all nodes
        workflow.add_node("perception", self._perception_node)
        workflow.add_node("memory", self._memory_node)
        workflow.add_node("world_model", self._world_model_node)
        workflow.add_node("decision", self._decision_node)
        workflow.add_node("action", self._action_node)
        workflow.add_node("introspection", self._introspection_node)

        # Linear chain (the loop will be handled in main.py)
        workflow.add_edge(START, "perception")
        workflow.add_edge("perception", "memory")
        workflow.add_edge("memory", "world_model")
        workflow.add_edge("world_model", "decision")
        workflow.add_edge("decision", "action")

        # Conditional jump after action:
        # - if reflection is needed -> introspection -> END
        # - otherwise immediately END
        def should_reflect(state: AgentState):
            if state.get("reflection_needed", False) or state.get("user_request") == "exit":
                return "introspection"
            return END

        workflow.add_conditional_edges(
            "action",
            should_reflect,
            {
                "introspection": "introspection",
                END: END
            }
        )
        # Finish execution
        workflow.add_edge("introspection", END)

        # Compilation
        graph = workflow.compile()

        # Visualization
        mermaid_code = graph.get_graph().draw_mermaid()
        with open("architecture_graph.mmd", "w", encoding="utf-8") as f:
            f.write(mermaid_code)

        return graph

    # ---------------------------------------------
    #                   Node Methods
    # ---------------------------------------------

    def _perception_node(self, state: AgentState) -> AgentState:
        return PerceptionModule().update_state(state)

    def _memory_node(self, state: AgentState) -> AgentState:
        return MemoryModule().update_state(state)

    def _world_model_node(self, state: AgentState) -> AgentState:
        return WorldModelModule().update_state(state)

    def _decision_node(self, state: AgentState) -> AgentState:
        return DecisionModule().update_state(state)

    def _action_node(self, state: AgentState) -> AgentState:
        return ActionModule().update_state(state)

    def _introspection_node(self, state: AgentState) -> AgentState:
        return IntrospectionModule().update_state(state)