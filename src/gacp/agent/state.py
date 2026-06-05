from typing import TypedDict, Annotated, Optional

def truncate_memory(memory: list, maxlen: int = 100) -> list:
    """Reducer for short memory: leaves the last maxlen records"""
    return memory[-maxlen:]

class AgentState(TypedDict):
    # ---- Perception and action ----
    current_observation: dict # object hypotheses (JSON)
    last_action: dict # abstract action
    last_outcome: dict # {success, reward, prediction_error}
    
    # ---- Memory ----
    short_term_memory: Annotated[list[dict], truncate_memory] # last N triplets
    long_term_memory_refs: list[str] # IDs of saved episodes (optional)
    
    # ---- World model ----
    active_hypotheses: dict # {hyp_id: {description, confidence, count}}
    predicted_next_observation: Optional[dict]
    prediction_confidence: float
    prediction_error: Optional[float]
    
    # ----Decision making ----
    current_plan: list[dict] # sequence of actions
    plan_step_index: int
    intrinsic_reward: float
    extrinsic_reward: float
    total_reward: float
    
    # ---- Introspection and the user ----
    reflection_needed: bool
    user_request: Optional[str]
    user_response: Optional[str] # response for TTS/chat
    reflection_log: list[dict] # reflection history
    
    # ---- Internal drivers ----
    internal_drives: dict # {curiosity, survival, competence}
    
    # ---- Meta information ----
    step_count: int
    episode_count: int
    game_id: str # ID of the current game
    is_exploring: bool
    exit_requested: bool # for graceful shutdown