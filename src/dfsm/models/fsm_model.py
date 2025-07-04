from typing import Dict, Optional, Set, Tuple

from pydantic import BaseModel, Field


class FSMModel(BaseModel):
    states: Set[str] = Field(..., min_length=1, description="The set of states")
    alphabet: Set[str] = Field(
        ..., min_length=1, description="The set of input symbols"
    )
    transition_functions: Dict[Tuple[str, str], str] = Field(
        ..., description="The transition functions"
    )
    initial_state: str = Field(..., min_length=1, description="The initial state")
    final_states: Optional[Set[str]] = Field(
        None, description="The set of final states"
    )
    state_outputs: Optional[Dict[str, str]] = Field(
        None, description="Moore machine outputs: state -> output"
    )
    transition_outputs: Optional[Dict[Tuple[str, str], str]] = Field(
        None, description="Mealy machine outputs: (state, input) -> output"
    )

    def validate_transitions(self) -> None:
        """
        Custom validation for transition function completeness.

        Args:
            self: the FSM model.

        Returns:
            None.

        Raises:
            ValueError: If the transition function is not valid.
        """
        for (state, symbol), next_state in self.transition_functions.items():
            if state not in self.states:
                raise ValueError(f"State '{state}' in transition not in states set")
            if next_state not in self.states:
                raise ValueError(f"Next state '{next_state}' not in states set")
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in alphabet")

        if self.initial_state not in self.states:
            raise ValueError(f"Initial state '{self.initial_state}' not in states set")

        if self.final_states:
            for state in self.final_states:
                if state not in self.states:
                    raise ValueError(f"Final state '{state}' not in states set")

        if self.state_outputs:
            for state in self.state_outputs:
                if state not in self.states:
                    raise ValueError(
                        f"State '{state}' in state_outputs not in states set"
                    )

        if self.transition_outputs:
            for state, symbol in self.transition_outputs:
                if state not in self.states:
                    raise ValueError(
                        f"State '{state}' in transition_outputs not in states set"
                    )
                if symbol not in self.alphabet:
                    raise ValueError(
                        f"Symbol '{symbol}' in transition_outputs not in alphabet"
                    )
