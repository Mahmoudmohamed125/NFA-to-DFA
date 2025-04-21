from NFA import NFA

def main() -> None:
    # states = {'1', '2', '3'}
    # alphabet = {'0', '1'}
    # transitions = {
    #     ('1', '1'): {'2'},
    #     ('1', 'ε'): {'3'},
    #     ('2', '0'): {'2', '3'},
    #     ('2', '1'): {'3'},
    #     ('3', '0'): {'1'}
    # }
    # start_state = '1'
    # final_states = {'1'}
    states = {'0', '1'}
    alphabet = {'a'}
    transitions = {
        ('0', 'ε'): {'1'},
        ('1', 'a'): {'1'},
        
    }
    start_state = '0'
    final_states = {'1'}
    nfa = NFA(states, alphabet, transitions, start_state, final_states)
    print("Constructed NFA:")
    print(nfa)

    closure_1 = nfa.get_epsilon_closure('1')
    print("\nEpsilon closure of state '1':", closure_1)

    dfa = nfa.to_dfa()
    print("\nConstructed DFA:")
    print(dfa)


if __name__ == "__main__":
    main()
