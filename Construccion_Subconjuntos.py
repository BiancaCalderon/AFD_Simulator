import json

# Función para calcular el ε-cierre de un conjunto de estados
def epsilon_closure(states, nfa_states):
    stack = list(states)
    closure = set(states)
    
    while stack:
        state = stack.pop()
        if '_' in nfa_states[state].transitions:  # '_' representa ε
            for next_state in nfa_states[state].transitions['_']:
                if next_state.name not in closure:
                    closure.add(next_state.name)
                    stack.append(next_state.name)
    
    return closure

# Función para movernos a nuevos estados dados un conjunto de estados y un símbolo
def move(states, symbol, nfa_states):
    move_set = set()
    for state in states:
        if symbol in nfa_states[state].transitions:
            for next_state in nfa_states[state].transitions[symbol]:
                move_set.add(next_state.name)
    
    return move_set

def subset_construction(nfa, nfa_states, alphabet):
    initial_closure = epsilon_closure([nfa.start.name], nfa_states)
    dfa_states = {frozenset(initial_closure): "q0"}  # Estado inicial del AFD
    unmarked_states = [frozenset(initial_closure)]
    dfa_transitions = {}
    dfa_accept_states = []
    
    state_count = 1
    while unmarked_states:
        current_set = unmarked_states.pop()
        current_state_name = dfa_states[frozenset(current_set)]
        
        for symbol in alphabet:
            move_set = move(current_set, symbol, nfa_states)
            closure_set = epsilon_closure(move_set, nfa_states)
            
            if frozenset(closure_set) not in dfa_states:
                dfa_states[frozenset(closure_set)] = f"q{state_count}"
                unmarked_states.append(frozenset(closure_set))
                state_count += 1
            
            if current_state_name not in dfa_transitions:
                dfa_transitions[current_state_name] = {}
            
            if closure_set:
                dfa_transitions[current_state_name][symbol] = dfa_states[frozenset(closure_set)]
    
    # Identificar los estados de aceptación
    for state_set, state_name in dfa_states.items():
        if nfa.end.name in state_set:
            dfa_accept_states.append(state_name)
    
    print(f"Construyendo AFD para el NFA con alfabeto: {alphabet}")
    return {
        "states": list(dfa_states.values()),
        "alphabet": list(alphabet),
        "transitions": dfa_transitions,
        "start": "q0",
        "accept": dfa_accept_states
    }

# Función para guardar el AFD en formato JSON
def save_dfa_to_json(dfa, filename):
    with open(filename, 'w') as file:
        json.dump(dfa, file, indent=4)
