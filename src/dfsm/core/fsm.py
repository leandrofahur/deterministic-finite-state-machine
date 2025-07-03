from typing import Any, Dict, List, Optional, Set, Tuple

import graphviz

from dfsm.models.fsm_model import FSMModel


# TODO: Extend the FSM class to include the output function to
# behave as a Moore/Mealy machine.
class FSM:
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transition_functions: Dict[Tuple[str, str], str],
        initial_state: str,
        final_states: Optional[Set[str]] = None,
        state_outputs: Optional[Dict[str, Any]] = None,
        transition_outputs: Optional[Dict[Tuple[str, str], Any]] = None,
    ):
        """
        Initialize the FSM with the given parameters.

        Args:
            states: the set of predefined states.
            alphabet: the set of possible input symbols.
            transition_functions: the dictionary containing the map between
                state and input symbol to a new state.
            initial_state: the state the machine starts in.
            final_states: the set of states the machine ends in (optional).
            state_outputs: the dictionary containing the output for each state.
            transition_outputs: the dictionary containing the output for each
                transition.
        """
        fsm_model = FSMModel(
            states=states,
            alphabet=alphabet,
            transition_functions=transition_functions,
            initial_state=initial_state,
            final_states=final_states,
            state_outputs=state_outputs,
            transition_outputs=transition_outputs,
        )

        # Validate the FSM model.
        fsm_model.validate_transitions()

        self.states = fsm_model.states
        self.alphabet = fsm_model.alphabet
        self.transition_functions = fsm_model.transition_functions
        self.initial_state = fsm_model.initial_state
        self.final_states = fsm_model.final_states
        self.state_outputs = fsm_model.state_outputs
        self.transition_outputs = fsm_model.transition_outputs

    def transitions(self, state: str, input_symbol: str) -> str:
        """
        Given the input symbol of the alphabet, returns the next state.

        Args:
            state: the current state.
            input_symbol: the input symbol.

        Returns:
            The next state.

        Raises:
            ValueError: If the state and input symbol are not in the
                transition function.
        """
        try:
            return self.transition_functions[(state, input_symbol)]
        except KeyError:
            raise ValueError(f"Transition ({state}, {input_symbol}) not defined")

    def _is_valid_state(self, state: str) -> bool:
        """
        Checks if the state is in the set of states.

        Args:
            state: the current state.

        Returns:
            True if the state is in the set of states, False otherwise.
        """
        return state in self.states

    def _is_valid_input(self, input_symbol: str) -> bool:
        """
        Checks if the input symbol is in the alphabet.

        Args:
            input_symbol: the input symbol.

        Returns:
            True if the input symbol is in the alphabet, False otherwise.
        """
        return input_symbol in self.alphabet

    def get_output(self, state: str, input_symbol: Optional[str] = None) -> Any:
        """
        Returns the output for the given state (Moore) or transition (Mealy).
        Mealy machines take precedence when both input_symbol and
        transition_outputs are provided.
        """
        if self.transition_outputs and input_symbol is not None:
            return self.transition_outputs.get((state, input_symbol))
        elif self.state_outputs:
            return self.state_outputs.get(state)
        return None

    def run(self, input_sequence: List[str], collect_outputs: bool = False) -> Any:
        """
        Runs the FSM with the given input sequence. Optionally collects outputs.
        Returns: the final state or (final state, outputs) if collect_outputs is True.
        """
        current_state = self.initial_state
        outputs = []
        for input_symbol in input_sequence:
            if not self._is_valid_input(input_symbol):
                raise ValueError(f"Invalid input symbol: {input_symbol}")
            if not self._is_valid_state(current_state):
                raise ValueError(f"Invalid state: {current_state}")
            output = self.get_output(current_state, input_symbol)
            if collect_outputs:
                outputs.append(output)
            current_state = self.transitions(current_state, input_symbol)
        if collect_outputs:
            # Optionally add Moore output for final state
            outputs.append(self.get_output(current_state))
            return current_state, outputs
        return current_state

    def visualize(self, filename: str, format: str = "png") -> None:
        """
        Visualizes the FSM using graphviz.
        """
        dot = graphviz.Digraph(format=format)
        # Initial state arrow
        dot.attr("node", shape="none")
        dot.node("start", label="")
        dot.attr("node", shape="circle")
        for state in self.states:
            shape = (
                "doublecircle"
                if self.final_states and state in self.final_states
                else "circle"
            )
            label = state
            if self.state_outputs and state in self.state_outputs:
                label += f"/ {self.state_outputs[state]}"
            dot.node(state, label=label, shape=shape)
        dot.edge("start", self.initial_state)
        for (state, symbol), next_state in self.transition_functions.items():
            label = symbol
            if self.transition_outputs and (state, symbol) in self.transition_outputs:
                label += f"/ {self.transition_outputs[(state, symbol)]}"
            dot.edge(state, next_state, label=label)
        dot.render(filename, view=False, cleanup=True)
