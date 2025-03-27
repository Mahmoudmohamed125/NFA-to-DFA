from typing import Dict, FrozenSet, List, Self, Set, Tuple

from DFA import DFA


class NFA:
    def __init__(
        self: Self, states: Set[str], alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Set[str]],
        start_state: str, final_states: Set[str]
    ) -> None:
        """
        Initialize an NFA.
        
        :param states: Set of states.
        :param alphabet: Set of symbols. Note: 'ε' is reserved for epsilon.
        :param transitions: Dictionary with keys as (state, symbol) tuples and values as sets of destination states.
        :param start_state: The start state.
        :param final_states: Set of accepting (final) states.
        """
        self.states: Set[str] = set(states)
        self.alphabet: Set[str] = set(alphabet)
        self.alphabet.add('ε')
        self.transitions: Dict[Tuple[str, str], Set[str]] = {
            key: set(dests) for key, dests in transitions.items()}
        self.start_state: str = start_state
        self.final_states: Set[str] = set(final_states)

    def get_epsilon_closure(self: Self, state: str) -> Set[str]:
        """Compute the epsilon closure of a given state."""
        closure: Set[str] = {state}
        stack: List[str] = [state]
        while stack:
            current = stack.pop()
            for next_state in self.transitions.get((current, 'ε'), set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def get_epsilon_closure_set(self: Self, states: Set[str]) -> Set[str]:
        """Compute the epsilon closure for a set of states."""
        closure: Set[str] = set()
        for state in states:
            closure |= self.get_epsilon_closure(state)
        return closure

    def to_dfa(self: Self) -> "DFA":
        """Convert the NFA to an equivalent DFA using subset construction."""
        initial: FrozenSet[str] = frozenset(
            self.get_epsilon_closure(self.start_state)
        )
        unmarked_states: List[FrozenSet[str]] = [initial]
        dfa_states: Set[FrozenSet[str]] = {initial}
        dfa_transitions: Dict[Tuple[FrozenSet[str], str], FrozenSet[str]] = {}

        while unmarked_states:
            current: FrozenSet[str] = unmarked_states.pop(0)
            for symbol in self.alphabet:
                if symbol == 'ε':
                    continue
                move_result: Set[str] = set()
                for state in current:
                    move_result |= self.transitions.get((state, symbol), set())
                next_state: FrozenSet[str] = frozenset(
                    self.get_epsilon_closure_set(move_result))
                dfa_transitions[(current, symbol)] = next_state
                if next_state not in dfa_states:
                    dfa_states.add(next_state)
                    unmarked_states.append(next_state)

        dead_state: FrozenSet[str] = frozenset()
        if dead_state not in dfa_states:
            dfa_states.add(dead_state)
            for symbol in self.alphabet - {'ε'}:
                dfa_transitions[(dead_state, symbol)] = dead_state

        dfa_final_states: Set[FrozenSet[str]] = {
            state for state in dfa_states if state & self.final_states}
        dfa_alphabet: Set[str] = self.alphabet - {'ε'}

        return DFA(dfa_states, dfa_alphabet, dfa_transitions, initial, dfa_final_states)

    def __repr__(self: Self) -> str:
        return (
            f"NFA(states={self.states}, alphabet={self.alphabet}, "
            f"start_state={self.start_state}, final_states={self.final_states}, "
            f"transitions={self.transitions})"
        )
