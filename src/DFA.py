from typing import Dict, FrozenSet, Self, Set, Tuple


class DFA:
    def __init__(
        self: Self, states: Set[FrozenSet[str]], alphabet: Set[str],
        transitions: Dict[Tuple[FrozenSet[str], str], FrozenSet[str]],
        start_state: FrozenSet[str], final_states: Set[FrozenSet[str]]
    ) -> None:
        """Initialize a DFA."""
        self.states: Set[FrozenSet[str]] = set(states)
        self.alphabet: Set[str] = set(alphabet)
        self.transitions: Dict[
            Tuple[FrozenSet[str], str], FrozenSet[str]
        ] = transitions
        self.start_state: FrozenSet[str] = start_state
        self.final_states: Set[FrozenSet[str]] = set(final_states)

    def __repr__(self: Self) -> str:
        def state_str(state: FrozenSet[str]) -> str:
            return "∅" if not state else "{" + ",".join(sorted(state)) + "}"
        
        trans_str: str = "\n".join(
            f"{state_str(s)} --{sym}--> {state_str(t)}"
            for (s, sym), t in self.transitions.items()
        )

        return (
            f"DFA:\nStart: {state_str(self.start_state)}\n"
            f"Final: {[state_str(s) for s in self.final_states]}\n"
            f"Transitions:\n{trans_str}"
        )
