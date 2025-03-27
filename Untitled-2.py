class NFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
    
    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            if (state, '') in self.transitions:
                for next_state in self.transitions[(state, '')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return frozenset(closure)
    
    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if (state, symbol) in self.transitions:
                next_states.update(self.transitions[(state, symbol)])
        return frozenset(next_states)
    
    def to_dfa(self):
        dfa_start = self.epsilon_closure({self.start_state})
        dfa_states = {dfa_start}
        dfa_transitions = {}
        dfa_final_states = set()
        unprocessed = [dfa_start]

        while unprocessed:
            current = unprocessed.pop()
            for symbol in self.alphabet:
                if symbol:
                    next_state = self.epsilon_closure(self.move(current, symbol))
                    if next_state:
                        dfa_transitions[(current, symbol)] = next_state
                        if next_state not in dfa_states:
                            dfa_states.add(next_state)
                            unprocessed.append(next_state)
            if any(state in self.final_states for state in current):
                dfa_final_states.add(current)

        return DFA(dfa_states, self.alphabet, dfa_transitions, dfa_start, dfa_final_states)

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
    
    def display(self):
        print("DFA States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Transitions:")
        for (state, symbol), next_state in self.transitions.items():
            print(f"  {state} --{symbol}--> {next_state}")
        print("Start State:", self.start_state)
        print("Final States:", self.final_states)

# Example usage
nfa_states = {'q0', 'q1', 'q2'}
nfa_alphabet = {'a', 'b'}
nfa_transitions = {
    ('q0', 'a'): {'q1'},
    ('q1', 'b'): {'q2'},
    ('q2', ''): {'q0'}  # Epsilon transition
}
nfa_start_state = 'q0'
nfa_final_states = {'q2'}

nfa = NFA(nfa_states, nfa_alphabet, nfa_transitions, nfa_start_state, nfa_final_states)
dfa = nfa.to_dfa()
dfa.display()
