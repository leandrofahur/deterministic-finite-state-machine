from typing import Dict, List, Set, Tuple, Optional

# TODO: Extend the FSM class to include the output function to behave as a Moore/Mealy machine.
class FSM:
    def __init__(self, states: Set[str], alphabet: Set[str], transition_functions: Dict[Tuple[str, str], str], initial_state: str, final_states: Optional[Set[str]] = None):
        '''
        Initialize the FSM with the given parameters.

        Args:
            states: the set of predefined states.
            alphabet: the set of possible input symbols.
            transition_functions: the dictionary containing the map between state and input symbol to a new state.
            initial_state: the state the machine starts in.
            (optional) final_states: the set of states the machine ends in.
        '''
        self.states = states
        self.alphabet = alphabet
        self.transition_functions = transition_functions
        self.initial_state = initial_state
        self.final_states = final_states        

    def transitions(self, state: str, input_symbol: str) -> str:
        '''
        Given the input symbol of the alphabet, returns the next state.

        Args:
            state: the current state.
            input_symbol: the input symbol.

        Returns:
            The next state.

        Raises:
            ValueError: If the state and input symbol are not in the transition function.
        '''
        try:
            return self.transition_functions[(state, input_symbol)]
        except KeyError:
            raise ValueError(f"Transition ({state}, {input_symbol}) not defined")
        
    def is_final_state(self, state: str) -> bool:
        '''
        Checks if the state is a final state.

        Args:
            state: the current state.

        Returns:
            True if the state is a final state, False otherwise.
        '''
        pass
    
    def is_valid_input(self, input_symbol: str) -> bool:
        '''
        Checks if the input symbol is in the alphabet.

        Args:
            input_symbol: the input symbol.

        Returns:
            True if the input symbol is in the alphabet, False otherwise.
        '''
        pass
        
    def run(self, input_sequence: List[str]) -> str:
        '''
        Runs the FSM with the given input sequence.

        Args:
            input_sequence: the sequence of input symbols

        Returns: the final state.
        '''
        
        current_state = self.initial_state        
        for input_symbol in input_sequence:            
            # print(f"({current_state}, {input_symbol}) -> {self.transitions(current_state, input_symbol)}")
            current_state = self.transitions(current_state, input_symbol)            
        return current_state    


# states = {'Locked', 'Unlocked'}
# alphabet = {'Coin', 'Push'}
# transition_functions = {
#     ('Locked','Push'): 'Locked',
#     ('Locked','Coin'): 'Unlocked',
#     ('Unlocked','Push'): 'Locked',
#     ('Unlocked','Coin'): 'Unlocked',
# }

# initial_state = 'Locked'
# final_states = {'Unlocked'}
# input_sequence = ['Push', 'Coin', 'Push', 'Push', 'Coin']


# fsm = FSM(states, alphabet, transition_functions, initial_state, final_states)
# fsm.run(input_sequence)

# print(fsm)


