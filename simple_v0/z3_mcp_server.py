# z3_mcp_server.py
from fastmcp import FastMCP
from z3 import Solver, parse_smt2_string, sat, unsat
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "mcp.json")

mcp = FastMCP("Z3 Solver", config_path=config_path)

@mcp.tool()
def solve(formula: str) -> dict:
    """
    Solve an SMT-LIB2 formula with Z3 and return sat/unsat/unknown
    plus a model when SAT.
    """
    s = Solver()
    s.add(parse_smt2_string(formula))
    result = s.check()

    if result == sat:
        model = {str(d): str(s.model()[d]) for d in s.model().decls()}
        return {"status": "sat", "model": model}
    if result == unsat:
        return {"status": "unsat"}
    return {"status": "unknown"}


def main():          
    mcp.run() 

if __name__ == "__main__":
    main()          # defaults to STDIO transport (Cursor-friendly)
