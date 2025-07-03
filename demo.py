#!/usr/bin/env python3
"""
Demo script for the DFSM library.
Shows how to create Moore/Mealy machines and generate visualizations.
"""

import os
import sys

from dfsm.core.fsm import FSM

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def demo_basic_fsm() -> None:
    """Demo: Basic FSM without outputs."""
    print("=== Basic FSM Demo ===")

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
    )

    # Run the FSM
    result = fsm.run(["Push", "Coin", "Push", "Push", "Coin"])
    print(f"Final state: {result}")

    # Generate visualization
    fsm.visualize("basic_fsm")
    print("Visualization saved as: basic_fsm.png")


def demo_moore_machine() -> None:
    """Demo: Moore machine (output per state)."""
    print("\n=== Moore Machine Demo ===")

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

    # Run with output collection
    final_state, outputs = fsm.run(["Timer", "Timer", "Timer"], collect_outputs=True)
    print(f"Final state: {final_state}")
    print(f"Outputs: {outputs}")

    # Generate visualization
    fsm.visualize("moore_traffic_light")
    print("Visualization saved as: moore_traffic_light.png")


def demo_mealy_machine() -> None:
    """Demo: Mealy machine (output per transition)."""
    print("\n=== Mealy Machine Demo ===")

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

    # Run with output collection
    final_state, outputs = fsm.run(["Coin", "Coin", "Select"], collect_outputs=True)
    print(f"Final state: {final_state}")
    print(f"Outputs: {outputs}")

    # Generate visualization
    fsm.visualize("mealy_vending_machine")
    print("Visualization saved as: mealy_vending_machine.png")


def demo_complex_fsm() -> None:
    """Demo: Complex FSM with multiple states."""
    print("\n=== Complex FSM Demo ===")

    fsm = FSM(
        states={"A", "B", "C", "D"},
        alphabet={"0", "1"},
        transition_functions={
            ("A", "0"): "B",
            ("A", "1"): "C",
            ("B", "0"): "C",
            ("B", "1"): "D",
            ("C", "0"): "D",
            ("C", "1"): "A",
            ("D", "0"): "A",
            ("D", "1"): "B",
        },
        initial_state="A",
        final_states={"D"},
        state_outputs={"A": "Alpha", "B": "Beta", "C": "Gamma", "D": "Delta"},
    )

    # Run with output collection
    final_state, outputs = fsm.run(["0", "1", "0", "1"], collect_outputs=True)
    print(f"Final state: {final_state}")
    print(f"Outputs: {outputs}")

    # Generate visualization
    fsm.visualize("complex_fsm", format="svg")
    print("Visualization saved as: complex_fsm.svg")


def main() -> None:
    print("DFSM Library Demo")
    print("=" * 50)

    try:
        demo_basic_fsm()
        demo_moore_machine()
        demo_mealy_machine()
        demo_complex_fsm()

        print("\n" + "=" * 50)
        print("All demos completed successfully!")
        print("Check the generated .png and .svg files for visualizations.")

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have graphviz installed:")
        print("  macOS: brew install graphviz")
        print("  Ubuntu: sudo apt-get install graphviz")
        print("  Windows: Download from https://graphviz.org/download/")


if __name__ == "__main__":
    main()
