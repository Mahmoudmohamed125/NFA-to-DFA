NFA to DFA Converter
Description
This project implements a conversion from a Non-Deterministic Finite Automaton (NFA) to a Deterministic Finite Automaton (DFA) using the subset construction algorithm. The conversion allows for handling epsilon (ε) transitions, ensuring the equivalent DFA correctly simulates the NFA’s behavior.

Features
Supports epsilon (ε) transitions.

Uses subset construction to generate the equivalent DFA.

Displays the DFA states, transitions, start state, and final states.

Requirements
Python 3.x

Installation
Clone the repository:

sh
Copy
Edit
git clone https://github.com/yourusername/nfa-to-dfa.git
cd nfa-to-dfa
Usage
Run the script:

sh
Copy
Edit
python nfa_to_dfa.py
Example NFA
States: {q0, q1, q2}

Alphabet: {a, b}

Transitions:

q0 --a--> q1

q1 --b--> q2

q2 --ε--> q0

Start State: q0

Final State: {q2}

Expected Output
The script prints the equivalent DFA, displaying:

States

Transitions

Start state

Final states
