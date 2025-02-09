def simulate_dfa(dfa, input_string):
    current_state = dfa['start']
    transitions = []
    total_transitions = 0

    for symbol in input_string:
        print(f"Processing symbol: {symbol} at state: {current_state}")
        if symbol in dfa['transitions'].get(current_state, {}):
            next_state = dfa['transitions'][current_state][symbol]
            transitions.append((current_state, symbol, next_state))
            current_state = next_state
            total_transitions += 1
        else:
            print(f"No transition for symbol: {symbol} at state: {current_state}")
            return "NO", transitions, total_transitions

    if current_state in dfa['accept']:
        print(f"Final state: {current_state} is an accepting state.")
        return "YES", transitions, total_transitions
    else:
        print(f"Final state: {current_state} is not an accepting state.")
        return "NO", transitions, total_transitions