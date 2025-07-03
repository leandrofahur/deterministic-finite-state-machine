"""Advanced tests for Moore/Mealy machine features and visualization."""

import os
import sys
import tempfile

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Import after path modification
from dfsm.core.fsm import FSM  # noqa: E402


class TestMooreMachine:
    """Test Moore machine functionality (output per state)."""

    def test_moore_machine_creation(self) -> None:
        """Test creating a Moore machine with state outputs."""
        fsm = FSM(
            states={"Locked", "Unlocked"},
            alphabet={"Coin", "Push"},
            transition_functions={
                ("Locked", "Push"): "Locked",
                ("Locked", "Coin"): "Unlocked",
                ("Unlocked", "Push"): "Locked",
                ("Unlocked", "Coin"): "Unlocked",
            },
            initial_state="Locked",
            final_states={"Unlocked"},
            state_outputs={"Locked": "Red", "Unlocked": "Green"},
        )

        assert fsm.get_output("Locked") == "Red"
        assert fsm.get_output("Unlocked") == "Green"
        assert fsm.get_output("Locked", "Coin") is None  # Mealy not configured

    def test_moore_machine_run_with_outputs(self) -> None:
        """Test running Moore machine and collecting outputs."""
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
            state_outputs={"A": "Alpha", "B": "Beta", "C": "Gamma"},
        )

        final_state, outputs = fsm.run(["0", "1", "0"], collect_outputs=True)
        assert final_state == "B"  # A->B->A->B
        assert outputs == [
            "Alpha",
            "Beta",
            "Alpha",
            "Beta",
        ]  # Initial + transitions + final


class TestMealyMachine:
    """Test Mealy machine functionality (output per transition)."""

    def test_mealy_machine_creation(self) -> None:
        """Test creating a Mealy machine with transition outputs."""
        fsm = FSM(
            states={"Locked", "Unlocked"},
            alphabet={"Coin", "Push"},
            transition_functions={
                ("Locked", "Push"): "Locked",
                ("Locked", "Coin"): "Unlocked",
                ("Unlocked", "Push"): "Locked",
                ("Unlocked", "Coin"): "Unlocked",
            },
            initial_state="Locked",
            final_states={"Unlocked"},
            transition_outputs={
                ("Locked", "Push"): "Beep",
                ("Locked", "Coin"): "Click",
                ("Unlocked", "Push"): "Click",
                ("Unlocked", "Coin"): "Beep",
            },
        )

        assert fsm.get_output("Locked", "Push") == "Beep"
        assert fsm.get_output("Locked", "Coin") == "Click"
        assert fsm.get_output("Locked") is None  # Moore not configured

    def test_mealy_machine_run_with_outputs(self) -> None:
        """Test running Mealy machine and collecting outputs."""
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
            transition_outputs={
                ("A", "0"): "X",
                ("A", "1"): "Y",
                ("B", "0"): "Z",
                ("B", "1"): "W",
            },
        )

        final_state, outputs = fsm.run(["0", "1", "0"], collect_outputs=True)
        assert final_state == "A"
        assert outputs == ["X", "W", "Z", None]  # Transitions + final (no Moore output)


class TestVisualization:
    """Test FSM visualization functionality."""

    def test_basic_visualization(self) -> None:
        """Test basic FSM visualization."""
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
            final_states={"B"},
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            fsm.visualize(tmp.name)
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)

    def test_moore_visualization(self) -> None:
        """Test Moore machine visualization with state outputs."""
        fsm = FSM(
            states={"Locked", "Unlocked"},
            alphabet={"Coin", "Push"},
            transition_functions={
                ("Locked", "Push"): "Locked",
                ("Locked", "Coin"): "Unlocked",
                ("Unlocked", "Push"): "Locked",
                ("Unlocked", "Coin"): "Unlocked",
            },
            initial_state="Locked",
            final_states={"Unlocked"},
            state_outputs={"Locked": "Red", "Unlocked": "Green"},
        )

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            fsm.visualize(tmp.name, format="svg")
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)

    def test_mealy_visualization(self) -> None:
        """Test Mealy machine visualization with transition outputs."""
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
            transition_outputs={
                ("A", "0"): "X",
                ("A", "1"): "Y",
                ("B", "0"): "Z",
                ("B", "1"): "W",
            },
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            fsm.visualize(tmp.name)
            assert os.path.exists(tmp.name)
            os.unlink(tmp.name)


class TestFSMExamples:
    """Real-world FSM examples demonstrating the library."""

    def test_traffic_light_example(self) -> None:
        """Example: Traffic light FSM with Moore outputs."""
        fsm = FSM(
            states={"Red", "Yellow", "Green"},
            alphabet={"Timer", "Emergency"},
            transition_functions={
                ("Red", "Timer"): "Green",
                ("Red", "Emergency"): "Red",
                ("Green", "Timer"): "Yellow",
                ("Green", "Emergency"): "Red",
                ("Yellow", "Timer"): "Red",
                ("Yellow", "Emergency"): "Red",
            },
            initial_state="Red",
            final_states={"Red", "Green", "Yellow"},
            state_outputs={"Red": "STOP", "Yellow": "CAUTION", "Green": "GO"},
        )

        # Simulate traffic light sequence
        final_state, outputs = fsm.run(
            ["Timer", "Timer", "Timer"], collect_outputs=True
        )
        assert final_state == "Red"
        assert outputs == ["STOP", "GO", "CAUTION", "STOP"]

    def test_vending_machine_example(self) -> None:
        """Example: Vending machine FSM with Mealy outputs."""
        fsm = FSM(
            states={"Idle", "Collecting", "Dispensing"},
            alphabet={"Coin", "Select", "Timeout"},
            transition_functions={
                ("Idle", "Coin"): "Collecting",
                ("Idle", "Select"): "Idle",
                ("Collecting", "Coin"): "Collecting",
                ("Collecting", "Select"): "Dispensing",
                ("Collecting", "Timeout"): "Idle",
                ("Dispensing", "Coin"): "Dispensing",
                ("Dispensing", "Select"): "Dispensing",
                ("Dispensing", "Timeout"): "Idle",
            },
            initial_state="Idle",
            final_states={"Idle", "Dispensing"},
            transition_outputs={
                ("Idle", "Coin"): "Display: $0.25",
                ("Collecting", "Coin"): "Display: $0.50",
                ("Collecting", "Select"): "Dispense item",
                ("Collecting", "Timeout"): "Return coins",
                ("Dispensing", "Timeout"): "Ready",
            },
        )

        # Simulate vending machine interaction
        final_state, outputs = fsm.run(["Coin", "Coin", "Select"], collect_outputs=True)
        assert final_state == "Dispensing"
        assert outputs == ["Display: $0.25", "Display: $0.50", "Dispense item", None]


if __name__ == "__main__":
    pytest.main([__file__])
