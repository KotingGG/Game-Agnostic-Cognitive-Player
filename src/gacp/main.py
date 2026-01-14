from agent.graph import build_workflow
from environments.timing import wait_for_next_game_tick

def main():
    agent_app = build_workflow()
    time = 0

    while True:
        #TODO: observation = capture_game_screen()  # Screen capture
        
        # Create an initial state
        initial_state = {
            "current_observation": {},
            "last_action": {},
            "last_outcome": {},

            "short_term_memory": [],
            "active_hypotheses": {},

            "internal_drives": {}
            # ... other fields
        }
        
        final_state = agent_app.invoke(initial_state)
        #TODO: execute_action(final_state["action_abstract"]) # Perform an action in the game
    
        print(f"Time: {time}")
        time += 1

        wait_for_next_game_tick() # Waiting for the next frame/tick of the game

if __name__ == "__main__":
    main()