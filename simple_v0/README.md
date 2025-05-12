# z3-mcp-server

An MCP server for solving SMT formulas using Z3 and FastMCP.

## Features
- Solve SMT-LIB2 formulas using Z3
- Enumerate all feasible solutions to a given formula
- Easily integrate with other MCP-compatible tools

## Installation

### Prerequisites
- Python 3.8+
- [Z3 Solver](https://github.com/Z3Prover/z3)
- [uv](https://github.com/astral-sh/uv) (recommended for fast installs)

### Setup
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>/simple_v0
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -e .
   # or, for binary-only z3-solver:
   pip install --only-binary :all: z3-solver
   pip install -e .
   ```

## Usage

Start the MCP server:
```bash
uv --directory ./simple_v0/.venv/bin/ run ./simple_v0/z3_mcp_server.py
```

The server will listen for MCP requests via STDIO (Cursor-friendly).

### Example: Solve an SMT-LIB2 formula

**Prime factorization of 35:**
```lisp
(declare-const x Int)
(declare-const y Int)
(assert (= (* x y) 35))
(assert (> x 1))
(assert (> y 1))
(check-sat)
(get-model)
```

### Example: Get all feasible solutions

**All integer pairs (x, y) with x > 0, y > 0, x*y < 25:**
```lisp
(declare-const x Int)
(declare-const y Int)
(assert (> x 0))
(assert (> y 0))
(assert (< (* x y) 25))
```

Call the `get_all_feasible_solns` tool with the above formula and an optional `max_solutions` parameter.

## Configuration

The server uses `mcp.json` to describe its tools and parameters. You can extend this file to add more tools or customize parameters.

## License

MIT 