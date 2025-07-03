"""Comprehensive tests for the FSM implementation."""

import os
import sys
from typing import Dict, Set, Tuple

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Import after path modification
from dfsm.core.fsm import FSM  # noqa: E402
from dfsm.models.fsm_model import FSMModel  # noqa: E402


class TestFSMBasic:
    """Basic FSM functionality tests."""

    @pytest.fixture  # type: ignore[misc]
    def simple_fsm_data(
        self,
    ) -> Tuple[Set[str], Set[str], Dict[Tuple[str, str], str], str, Set[str]]:
        """Fixture for simple FSM test data."""
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
        return states, alphabet, transition_functions, initial_state, final_states

    @pytest.fixture  # type: ignore[misc]
    def simple_fsm(
        self,
        simple_fsm_data: Tuple[
            Set[str], Set[str], Dict[Tuple[str, str], str], str, Set[str]
        ],
    ) -> FSM:
        """Fixture for simple FSM instance."""
        (
            states,
            alphabet,
            transition_functions,
            initial_state,
            final_states,
        ) = simple_fsm_data
        return FSM(
            states=states,
            alphabet=alphabet,
            transition_functions=transition_functions,
            initial_state=initial_state,
            final_states=final_states,
        )

    def test_fsm_creation(self, simple_fsm_data: Dict) -> None:
        """Test that FSM can be created with valid parameters."""
        fsm = FSM(**simple_fsm_data)

        assert fsm.states == simple_fsm_data["states"]
        assert fsm.alphabet == simple_fsm_data["alphabet"]
        assert fsm.initial_state == simple_fsm_data["initial_state"]
        assert fsm.final_states == simple_fsm_data["final_states"]

    def test_fsm_creation_without_final_states(self) -> None:
        """Test FSM creation without final states."""
        fsm = FSM(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "B",
                ("A", "1"): "A",
                ("B", "0"): "A",
                ("B", "1"): "B",
            },
            initial_state="A",
        )
        assert fsm.final_states is None

    def test_transitions_valid(self, simple_fsm: FSM) -> None:
        """Test valid transitions."""
        assert simple_fsm.transitions("Locked", "Coin") == "Unlocked"
        assert simple_fsm.transitions("Locked", "Push") == "Locked"
        assert simple_fsm.transitions("Unlocked", "Coin") == "Unlocked"
        assert simple_fsm.transitions("Unlocked", "Push") == "Locked"

    def test_transitions_invalid(self, simple_fsm: FSM) -> None:
        """Test invalid transitions raise ValueError."""
        with pytest.raises(
            ValueError, match="Transition \\(InvalidState, Coin\\) not defined"
        ):
            simple_fsm.transitions("InvalidState", "Coin")

        with pytest.raises(
            ValueError, match="Transition \\(Locked, InvalidSymbol\\) not defined"
        ):
            simple_fsm.transitions("Locked", "InvalidSymbol")

    def test_is_valid_state(self, simple_fsm: FSM) -> None:
        """Test state validation."""
        assert simple_fsm._is_valid_state("Locked") is True
        assert simple_fsm._is_valid_state("Unlocked") is True
        assert simple_fsm._is_valid_state("InvalidState") is False

    def test_is_valid_input(self, simple_fsm: FSM) -> None:
        """Test input validation."""
        assert simple_fsm._is_valid_input("Coin") is True
        assert simple_fsm._is_valid_input("Push") is True
        assert simple_fsm._is_valid_input("InvalidSymbol") is False

    def test_run_valid_sequence(self, simple_fsm: FSM) -> None:
        """Test running FSM with valid input sequence."""
        result = simple_fsm.run(["Push", "Coin", "Push", "Push", "Coin"])
        assert result == "Unlocked"

    def test_run_empty_sequence(self, simple_fsm: FSM) -> None:
        """Test running FSM with empty input sequence."""
        result = simple_fsm.run([])
        assert result == "Locked"  # Should return initial state

    def test_run_single_transition(self, simple_fsm: FSM) -> None:
        """Test running FSM with single transition."""
        result = simple_fsm.run(["Coin"])
        assert result == "Unlocked"

    def test_run_invalid_input_symbol(self, simple_fsm: FSM) -> None:
        """Test running FSM with invalid input symbol."""
        with pytest.raises(ValueError, match="Invalid input symbol: InvalidSymbol"):
            simple_fsm.run(["Coin", "InvalidSymbol"])

    def test_run_complex_sequence(self, simple_fsm: FSM) -> None:
        """Test running FSM with complex sequence."""
        # Test a longer sequence that exercises multiple transitions
        result = simple_fsm.run(["Push", "Coin", "Push", "Coin", "Push", "Coin"])
        assert result == "Unlocked"


class TestFSMModelValidation:
    """Test FSM model validation."""

    def test_valid_fsm_model(self) -> None:
        """Test valid FSM model creation."""
        model = FSMModel(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "B",
                ("A", "1"): "A",
                ("B", "0"): "A",
                ("B", "1"): "B",
            },
            initial_state="A",
            final_states={"B"},
            state_outputs=None,
            transition_outputs=None,
        )
        model.validate_transitions()  # Should not raise

    def test_invalid_state_in_transition(self) -> None:
        """Test validation fails with invalid state in transition."""
        model = FSMModel(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={("A", "0"): "B", ("InvalidState", "1"): "A"},
            initial_state="A",
            final_states=None,
            state_outputs=None,
            transition_outputs=None,
        )
        with pytest.raises(
            ValueError, match="State 'InvalidState' in transition not in states set"
        ):
            model.validate_transitions()

    def test_invalid_next_state(self) -> None:
        """Test validation fails with invalid next state."""
        model = FSMModel(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={("A", "0"): "B", ("A", "1"): "InvalidNextState"},
            initial_state="A",
            final_states=None,
            state_outputs=None,
            transition_outputs=None,
        )
        with pytest.raises(
            ValueError, match="Next state 'InvalidNextState' not in states set"
        ):
            model.validate_transitions()

    def test_invalid_symbol_in_transition(self) -> None:
        """Test validation fails with invalid symbol in transition."""
        model = FSMModel(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={("A", "0"): "B", ("A", "InvalidSymbol"): "A"},
            initial_state="A",
            final_states=None,
            state_outputs=None,
            transition_outputs=None,
        )
        with pytest.raises(ValueError, match="Symbol 'InvalidSymbol' not in alphabet"):
            model.validate_transitions()

    def test_invalid_initial_state(self) -> None:
        """Test validation fails with invalid initial state."""
        model = FSMModel(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "B",
                ("A", "1"): "A",
                ("B", "0"): "A",
                ("B", "1"): "B",
            },
            initial_state="InvalidInitialState",
            final_states=None,
            state_outputs=None,
            transition_outputs=None,
        )
        with pytest.raises(
            ValueError, match="Initial state 'InvalidInitialState' not in states set"
        ):
            model.validate_transitions()

    def test_invalid_final_state(self) -> None:
        """Test validation fails with invalid final state."""
        model = FSMModel(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "B",
                ("A", "1"): "A",
                ("B", "0"): "A",
                ("B", "1"): "B",
            },
            initial_state="A",
            final_states={"InvalidFinalState"},
            state_outputs=None,
            transition_outputs=None,
        )
        with pytest.raises(
            ValueError, match="Final state 'InvalidFinalState' not in states set"
        ):
            model.validate_transitions()

    def test_multiple_invalid_final_states(self) -> None:
        """Test validation fails with multiple invalid final states."""
        model = FSMModel(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "B",
                ("A", "1"): "A",
                ("B", "0"): "A",
                ("B", "1"): "B",
            },
            initial_state="A",
            final_states={"A", "InvalidFinalState"},
            state_outputs=None,
            transition_outputs=None,
        )
        with pytest.raises(
            ValueError, match="Final state 'InvalidFinalState' not in states set"
        ):
            model.validate_transitions()


class TestFSMEdgeCases:
    """Test FSM edge cases and error conditions."""

    def test_single_state_fsm(self) -> None:
        """Test FSM with single state."""
        fsm = FSM(
            states={"A"},
            alphabet={"0"},
            transition_functions={("A", "0"): "A"},
            initial_state="A",
            final_states={"A"},
        )
        result = fsm.run(["0", "0", "0"])
        assert result == "A"

    def test_single_symbol_alphabet(self) -> None:
        """Test FSM with single symbol alphabet."""
        fsm = FSM(
            states={"A", "B"},
            alphabet={"0"},
            transition_functions={("A", "0"): "B", ("B", "0"): "A"},
            initial_state="A",
        )
        result = fsm.run(["0", "0"])
        assert result == "A"

    def test_self_looping_states(self) -> None:
        """Test FSM with self-looping states."""
        fsm = FSM(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "A",
                ("A", "1"): "B",
                ("B", "0"): "A",
                ("B", "1"): "B",
            },
            initial_state="A",
        )
        result = fsm.run(["0", "0", "0"])  # Stay in A
        assert result == "A"
        result = fsm.run(["1", "1", "1"])  # Go to B and stay
        assert result == "B"

    def test_complex_transition_sequence(self) -> None:
        """Test FSM with complex transition sequence."""
        fsm = FSM(
            states={"A", "B", "C"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "B",
                ("A", "1"): "C",
                ("B", "0"): "C",
                ("B", "1"): "A",
                ("C", "0"): "A",
                ("C", "1"): "B",
            },
            initial_state="A",
        )
        result = fsm.run(["0", "1", "0", "1", "0"])
        assert result == "B"  # A->B->A->B->A->B

    def test_error_handling_in_run_method(self) -> None:
        """Test error handling in run method."""
        fsm = FSM(
            states={"A", "B"},
            alphabet={"0", "1"},
            transition_functions={
                ("A", "0"): "B",
                ("A", "1"): "A",
                ("B", "0"): "A",
                ("B", "1"): "B",
            },
            initial_state="A",
        )

        # Test invalid input symbol
        with pytest.raises(ValueError, match="Invalid input symbol: 2"):
            fsm.run(["0", "2", "1"])


if __name__ == "__main__":
    pytest.main([__file__])
