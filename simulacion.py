def simulate_dfa(dfa, input_string):
    current_state = dfa['start']
    transitions = []

    for symbol in input_string:
        # Verifica si el símbolo esta en las transiciones del estado actual
        if symbol in dfa['transitions'][current_state]:
            next_state = dfa['transitions'][current_state][symbol]
            transitions.append((current_state, symbol, next_state))
            current_state = next_state
        else:
            # No hay transición para el símbolo en el estado actual
            return "NO", transitions

    # Verifica si el estado final es un estado de aceptación
    if current_state in dfa['accept']:
        return "YES", transitions
    else:
        return "NO", transitions