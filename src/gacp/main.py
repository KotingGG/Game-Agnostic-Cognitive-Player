# =============================================
#               The Entry Point
# =============================================
from agent.graph import Graph
from environments.timing import wait_for_next_game_tick

def main():
    print("="*40)
    print("Game Agnostic Congitive Player")
    print("="*40+'\n')

    agent_app = Graph().build_workflow()
    time = 0

    # Initial state
    current_state = {
        "current_observation": {},
        "last_action": {},
        "last_outcome": {},
        "short_term_memory": [],
        "active_hypotheses": {},
        "internal_drives": {},
        "reflection_needed": False,
        "user_request": None,
    }

    try:
        while True:
            # Get raw data from the game
            # raw_obs = capture_game_screen()
            current_state["current_observation"] = {}  # stub

            # Run the graph in stream mode (one pass)
            final_state = None
            for event in agent_app.stream(current_state):
                # event looks like {node_name: state_snapshot}
                for node_name, node_state in event.items():
                    print(f"Node completed: {node_name}")
                    final_state = node_state   # last state – after action or introspection

            if final_state is None:
                final_state = current_state

            # Extract the abstract action (if any)
            action_abstract = final_state.get("last_action", {})
            # TODO: execute_action(action_abstract)  # send to the game

            # Update the state for the next tick
            current_state = final_state.copy()
            # Resetting temporary flags so as not to get stuck in introspection
            current_state["reflection_needed"] = False
            if current_state.get("user_request") == "exit":
                print("A logout command was received from the user. Finishing the job.")
                break

            print(f"Time: {time}")
            time += 1

            wait_for_next_game_tick()

    except KeyboardInterrupt:
        print(f"\nProgram stopped by user")

if __name__ == "__main__":
    main()