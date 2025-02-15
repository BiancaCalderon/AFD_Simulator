import json
import time  # Import time module for timing the simulation
from regex_conversion import shunting_yard, insert_concatenation_operators, thompson_construction, generate_adjacency_matrix, print_adjacency_matrix
from Construccion_Subconjuntos import subset_construction
from Minimization import minimize_dfa, save_minimized_dfa_to_json
from graphviz import Digraph  # Importar la biblioteca graphviz para dibujar el diagrama

def simulate_dfa(dfa, input_string):
    current_state = dfa['start']
    transitions = []

    start_time = time.time()  # Start timing the simulation

    for symbol in input_string:
        if symbol in dfa['transitions'][current_state]:
            next_state = dfa['transitions'][current_state][symbol]
            transitions.append((current_state, symbol, next_state))  # Record the transition
            current_state = next_state
        else:
            end_time = time.time()  # End timing the simulation
            elapsed_time = end_time - start_time
            return "NO", transitions, elapsed_time  # Transición inválida, cadena no aceptada

    end_time = time.time()  # End timing the simulation
    elapsed_time = end_time - start_time

    if current_state in dfa['accept']:
        return "YES", transitions, elapsed_time
    else:
        return "NO", transitions, elapsed_time

# Main code
# Paso 1: Solicitar expresión regular y convertirla a postfix
regex = input("Ingresa una expresión regular: ")
regex = insert_concatenation_operators(regex)
postfix = shunting_yard(regex)
print("Postfix:", postfix)

# Paso 2: Construir el NFA con el algoritmo de Thompson
nfa, states = thompson_construction(postfix)
print("AFN construido.")
adjacency_matrix = generate_adjacency_matrix(states)
print("Matriz de adyacencia del NFA:")
print_adjacency_matrix(adjacency_matrix, states)

# Paso 3: Convertir el NFA a AFD utilizando el algoritmo de construcción de subconjuntos
alphabet = set(char for char in regex if char.isalnum() or char == '_')  # Extraer el alfabeto de la expresión regular
dfa = subset_construction(nfa, {state.name: state for state in states}, alphabet)
print("AFD construido.")

# Paso 4: Minimizar el AFD
minimized_dfa = minimize_dfa(dfa)
print("AFD minimizado:")

# Mostrar los componentes del AFD minimizado
print("Estados:", minimized_dfa["states"])
print("Alfabeto:", minimized_dfa["alphabet"])
print("Transiciones:")
for state, transitions in minimized_dfa["transitions"].items():
    for symbol, target_state in transitions.items():
        print(f"{state} -- {symbol} --> {target_state}")
print("Estado inicial:", minimized_dfa["start"])
print("Estados de aceptación:", minimized_dfa["accept"])

# Paso 5: Guardar el AFD minimizado con todos los detalles en un archivo JSON
dfa_data = {
    "states": minimized_dfa["states"],
    "alphabet": minimized_dfa["alphabet"],
    "transitions": minimized_dfa["transitions"],
    "start": minimized_dfa["start"],
    "accept": minimized_dfa["accept"]
}

# Guardar el resultado en un archivo JSON
with open("minimized_dfa_complete.json", 'w') as file:
    json.dump(dfa_data, file, indent=4)

print("El AFD minimizado completo ha sido guardado en 'minimized_dfa_complete.json'.")

# Paso 6: Simular el AFD con una cadena de entrada
input_string = input("Ingresa la cadena a validar: ")
result, transitions, elapsed_time = simulate_dfa(minimized_dfa, input_string)
print(f"La cadena '{input_string}' es {'aceptada' if result == 'YES' else 'no aceptada'} por el AFD.")
print(f"Tiempo de validación: {elapsed_time:.6f} segundos")

# Print the total number of transitions
print(f"Total de transiciones realizadas: {len(transitions)}")

print("Transiciones realizadas durante la validación:")
if transitions:
    for transition in transitions:
        print(transition)
else:
    print("No se realizaron transiciones.")

# Paso 7: Dibujar el diagrama del AFD minimizado
def draw_minimized_dfa(dfa):
    dot = Digraph()

    # Agregar estados al diagrama
    for state in dfa["states"]:
        if state in dfa["accept"]:
            dot.node(state, state, shape='doublecircle')  # Estados de aceptación
        else:
            dot.node(state, state)  # Estados normales

    # Agregar transiciones al diagrama
    for state, transitions in dfa["transitions"].items():
        for symbol, target_state in transitions.items():
            dot.edge(state, target_state, label=symbol)

    dot.render('minimized_dfa', format='png', cleanup=True)  # Guardar el diagrama como imagen PNG
    print("Diagrama del AFD minimizado guardado como 'minimized_dfa.png'.")

# Llamar a la función para dibujar el diagrama después de minimizar el AFD
draw_minimized_dfa(minimized_dfa)