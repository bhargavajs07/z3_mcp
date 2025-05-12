# z3_mcp_server.py
from fastmcp import FastMCP
from z3 import Solver, parse_smt2_string, sat, unsat, Or
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

@mcp.tool()
def get_all_feasible_solns(formula: str, max_solutions: int = 100) -> dict:
    """
    Return all feasible solutions (up to max_solutions) that satisfy the given SMT-LIB2 formula.
    """
    s = Solver()
    s.add(parse_smt2_string(formula))
    solutions = []
    count = 0
    while s.check() == sat and count < max_solutions:
        m = s.model()
        model_dict = {str(d): int(str(m[d])) for d in m.decls()}
        solutions.append(model_dict)
        # Add a blocking clause to prevent this solution from appearing again
        s.add(Or([d() != m[d] for d in m.decls()]))
        count += 1
    max_reached = count == max_solutions
    return {"status": "ok", "num_solutions": len(solutions), "max_solutions_used": max_solutions, "max_solutions_reached": max_reached, "solutions": solutions}

def main():          
    mcp.run() 

if __name__ == "__main__":
    main()          # defaults to STDIO transport (Cursor-friendly)
