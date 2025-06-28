"""Basic tests for the FSM implementation."""

import os
import sys

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Import after path modification
from dfsm.core.fsm import FSM  # noqa: E402


class TestFSMBasic:
    """Basic FSM functionality tests."""

    def test_fsm_creation(self) -> None:
        """Test that FSM can be created with valid parameters."""
        states = {"Locked", "Unlocked"}
        alphabet = {"Coin", "Push"}
        transition_functions = {
            ("Locked", "Push"): "Locked",
            ("Locked", "Coin"): "Unlocked",
            ("Unlocked", "Push"): "Locked",
            ("Unlocked", "Coin"): "Unlocked",
        }
        initial_state = "Locked"
        final_states = {"Unlocked"}

        fsm = FSM(
            states=states,
            alphabet=alphabet,
            transition_functions=transition_functions,
            initial_state=initial_state,
            final_states=final_states,
        )

        assert fsm.states == states
        assert fsm.alphabet == alphabet
        assert fsm.initial_state == initial_state
        assert fsm.final_states == final_states


if __name__ == "__main__":
    pytest.main([__file__])
