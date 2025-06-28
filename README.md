# Deterministic Finite State Machine (DFSM)

A modular, extensible, and class-based Deterministic Finite State Machine library for Python.

## Features

- ✅ Type-safe implementation with Pydantic validation
- ✅ Comprehensive error handling and validation
- ✅ Educational examples and documentation
- ✅ Professional code quality standards
- ✅ Extensive test coverage

## Quick Start

```python
from dfsm import FSM

# Create a simple FSM
fsm = FSM(
    states={'Locked', 'Unlocked'},
    alphabet={'Coin', 'Push'},
    transition_functions={
        ('Locked', 'Push'): 'Locked',
        ('Locked', 'Coin'): 'Unlocked',
        ('Unlocked', 'Push'): 'Locked',
        ('Unlocked', 'Coin'): 'Unlocked',
    },
    initial_state='Locked',
    final_states={'Unlocked'}
)

# Run the FSM
result = fsm.run(['Push', 'Coin', 'Push', 'Push', 'Coin'])
print(f"Final state: {result}")  # Output: Final state: Unlocked
```

## Development

### Setup

1. Clone the repository
2. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Quality Tools

This project uses several quality tools to maintain high code standards:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing with coverage
- **pre-commit**: Automated quality checks

### Commands

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/

# Run tests
pytest

# Run all quality checks
pre-commit run --all-files
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `pre-commit run --all-files`
5. Run tests: `pytest`
6. Submit a pull request

## License

MIT License - see LICENSE file for details.