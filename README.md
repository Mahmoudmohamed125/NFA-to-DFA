# Regex to NFA & NFA to DFA Converter

## Overview
This project implements a converter that transforms a regular expression into a Non-deterministic Finite Automaton (NFA) and further converts the NFA into a Deterministic Finite Automaton (DFA). The implementation follows **Thompson’s construction** for regex-to-NFA conversion and **subset construction** for NFA-to-DFA conversion.

## Features
✔ Convert a given regular expression to an NFA  
✔ Convert the generated NFA to a DFA  
✔ Supports **concatenation (.), union (|), and Kleene star (*)**  
✔ Uses **epsilon closures** for efficient NFA-to-DFA conversion  
✔ Implements a **state-based approach** for managing transitions  

## How It Works
### **Regex to NFA Conversion**
- Constructs an NFA using **Thompson's construction**.
- Uses a **stack-based** approach to build the automaton.

### **NFA to DFA Conversion**
- Computes **epsilon closures** of NFA states.
- Uses the **subset construction** algorithm to generate the DFA.

## Code Structure
- `State` class → Represents a state in an automaton.  
- `NFA` class → Converts a regex into an NFA.  
- `DFA` class → Converts an NFA into a DFA.  
- `epsilon_closure` function → Computes the epsilon closure of a set of states.  

## Example Usage
```python
regex = "ab|*"  # Represents (a|b)* in postfix notation
nfa = NFA.from_regex(regex)
dfa = DFA.from_nfa(nfa)
print("DFA Created Successfully")
