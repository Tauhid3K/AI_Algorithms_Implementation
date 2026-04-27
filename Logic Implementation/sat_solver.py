"""
Advanced Logic Implementation - Satisfiability (SAT) Solver
Implements SAT solving algorithms for Boolean formulas.
"""

from typing import Dict, List, Tuple, Optional, Set
import itertools


class SATFormula:
    """Represents a Boolean formula in Conjunctive Normal Form (CNF)."""
    
    def __init__(self, clauses: List[List[Tuple[bool, str]]]):
        """
        Initialize SAT formula in CNF.
        
        Args:
            clauses: List of clauses, each clause is a list of (negated, variable) tuples
        """
        self.clauses = clauses
        self.variables = self._extract_variables()
    
    def _extract_variables(self) -> Set[str]:
        """Extract all variables from the formula."""
        variables = set()
        for clause in self.clauses:
            for _, var in clause:
                variables.add(var)
        return variables
    
    def __repr__(self):
        clause_strs = []
        for clause in self.clauses:
            literals = []
            for negated, var in clause:
                if negated:
                    literals.append(f"¬{var}")
                else:
                    literals.append(var)
            clause_strs.append("(" + " ∨ ".join(literals) + ")")
        return " ∧ ".join(clause_strs)
    
    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        """Evaluate formula with given assignment."""
        for clause in self.clauses:
            clause_result = False
            for negated, var in clause:
                literal = assignment.get(var, False)
                if negated:
                    literal = not literal
                clause_result = clause_result or literal
            
            if not clause_result:
                return False
        
        return True


class SimpleSATSolver:
    """Simple SAT solver using brute force search."""
    
    @staticmethod
    def solve(formula: SATFormula) -> Optional[Dict[str, bool]]:
        """
        Solve SAT problem by trying all assignments.
        
        Args:
            formula: SAT formula in CNF
            
        Returns:
            Satisfying assignment or None if unsatisfiable
        """
        variables = sorted(formula.variables)
        
        # Try all possible assignments
        for values in itertools.product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            if formula.evaluate(assignment):
                return assignment
        
        return None
    
    @staticmethod
    def find_all_solutions(formula: SATFormula) -> List[Dict[str, bool]]:
        """Find all satisfying assignments."""
        solutions = []
        variables = sorted(formula.variables)
        
        for values in itertools.product([False, True], repeat=len(variables)):
            assignment = dict(zip(variables, values))
            if formula.evaluate(assignment):
                solutions.append(assignment)
        
        return solutions


class DPLL:
    """DPLL (Davis-Putnam-Logemann-Loveland) SAT solver."""
    
    def __init__(self):
        self.call_count = 0
    
    def solve(self, formula: SATFormula) -> Optional[Dict[str, bool]]:
        """Solve using DPLL algorithm."""
        self.call_count = 0
        assignment = {}
        return self._dpll_recursive(formula.clauses, assignment, formula.variables)
    
    def _dpll_recursive(self, clauses: List, assignment: Dict, 
                       variables: Set) -> Optional[Dict]:
        """Recursive DPLL solver."""
        self.call_count += 1
        
        # Check for satisfiability
        if self._is_satisfiable(clauses, assignment):
            return assignment
        
        # Check for unsatisfiability
        if self._has_empty_clause(clauses, assignment):
            return None
        
        # Unit propagation
        unit_var = self._find_unit_clause(clauses, assignment)
        if unit_var is not None:
            new_assignment = assignment.copy()
            new_assignment[unit_var[0]] = not unit_var[1]
            result = self._dpll_recursive(clauses, new_assignment, variables)
            if result is not None:
                return result
        
        # Pure literal elimination
        pure_var = self._find_pure_literal(clauses, assignment, variables)
        if pure_var is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_var[0]] = pure_var[1]
            result = self._dpll_recursive(clauses, new_assignment, variables)
            if result is not None:
                return result
        
        # Choose variable for branching
        unassigned = [v for v in variables if v not in assignment]
        if not unassigned:
            return assignment if self._evaluate_clauses(clauses, assignment) else None
        
        var = unassigned[0]
        
        # Try variable = True
        new_assignment = assignment.copy()
        new_assignment[var] = True
        result = self._dpll_recursive(clauses, new_assignment, variables)
        if result is not None:
            return result
        
        # Try variable = False
        new_assignment = assignment.copy()
        new_assignment[var] = False
        result = self._dpll_recursive(clauses, new_assignment, variables)
        return result
    
    def _is_satisfiable(self, clauses: List, assignment: Dict) -> bool:
        """Check if all clauses are satisfied."""
        for clause in clauses:
            clause_result = False
            for negated, var in clause:
                if var not in assignment:
                    clause_result = None
                    break
                
                literal = assignment[var]
                if negated:
                    literal = not literal
                clause_result = clause_result or literal
            
            if clause_result is None:
                return False
        
        return True
    
    def _has_empty_clause(self, clauses: List, assignment: Dict) -> bool:
        """Check if there's an empty clause (unsatisfiable)."""
        for clause in clauses:
            clause_satisfied = False
            clause_all_assigned = True
            
            for negated, var in clause:
                if var not in assignment:
                    clause_all_assigned = False
                    break
                
                literal = assignment[var]
                if negated:
                    literal = not literal
                
                if literal:
                    clause_satisfied = True
                    break
            
            if clause_all_assigned and not clause_satisfied:
                return True
        
        return False
    
    def _find_unit_clause(self, clauses: List, assignment: Dict) -> Optional[Tuple]:
        """Find a unit clause (clause with one unassigned literal)."""
        for clause in clauses:
            unassigned_literals = []
            
            for negated, var in clause:
                if var not in assignment:
                    unassigned_literals.append((var, negated))
            
            if len(unassigned_literals) == 1:
                var, negated = unassigned_literals[0]
                return (var, negated)
        
        return None
    
    def _find_pure_literal(self, clauses: List, assignment: Dict, 
                          variables: Set) -> Optional[Tuple]:
        """Find a pure literal (appears with only one polarity)."""
        literal_polarities = {}
        
        for clause in clauses:
            for negated, var in clause:
                if var not in assignment:
                    if var not in literal_polarities:
                        literal_polarities[var] = set()
                    literal_polarities[var].add(negated)
        
        for var, polarities in literal_polarities.items():
            if len(polarities) == 1:
                negated = list(polarities)[0]
                return (var, not negated)
        
        return None
    
    def _evaluate_clauses(self, clauses: List, assignment: Dict) -> bool:
        """Evaluate all clauses."""
        for clause in clauses:
            clause_result = False
            for negated, var in clause:
                literal = assignment.get(var, False)
                if negated:
                    literal = not literal
                clause_result = clause_result or literal
            
            if not clause_result:
                return False
        
        return True


class ThreeColorability:
    """Graph 3-colorability problem solver using SAT."""
    
    @staticmethod
    def to_sat_formula(edges: List[Tuple[int, int]], num_nodes: int) -> SATFormula:
        """
        Convert graph coloring problem to SAT.
        
        Args:
            edges: List of edges (u, v)
            num_nodes: Number of nodes
            
        Returns:
            SAT formula
        """
        # Variables: node_i_color_j where i in [0, num_nodes), j in [0, 3)
        # Colors: 0 (Red), 1 (Green), 2 (Blue)
        
        clauses = []
        
        # Each node must have exactly one color
        for i in range(num_nodes):
            # At least one color
            clause = [(False, f"c{i}_0"), (False, f"c{i}_1"), (False, f"c{i}_2")]
            clauses.append(clause)
            
            # At most one color
            clauses.append([(True, f"c{i}_0"), (True, f"c{i}_1")])
            clauses.append([(True, f"c{i}_0"), (True, f"c{i}_2")])
            clauses.append([(True, f"c{i}_1"), (True, f"c{i}_2")])
        
        # Adjacent nodes must have different colors
        for u, v in edges:
            for color in range(3):
                # At least one of u or v must not have this color
                clauses.append([(True, f"c{u}_{color}"), (True, f"c{v}_{color}")])
        
        return SATFormula(clauses)
    
    @staticmethod
    def solve_coloring(edges: List[Tuple[int, int]], num_nodes: int) -> Optional[Dict]:
        """Solve graph 3-coloring problem."""
        formula = ThreeColorability.to_sat_formula(edges, num_nodes)
        solver = DPLL()
        return solver.solve(formula)


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("SAT SOLVER IMPLEMENTATIONS")
    print("="*60)
    
    # Example 1: Simple SAT problem
    print("\n1. Simple SAT Problem:")
    print("-" * 60)
    
    # (A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)
    clauses1 = [
        [(False, 'A'), (False, 'B')],
        [(True, 'A'), (False, 'C')],
        [(True, 'B'), (True, 'C')]
    ]
    
    formula1 = SATFormula(clauses1)
    print(f"Formula: {formula1}")
    
    solver_simple = SimpleSATSolver()
    solution1 = solver_simple.solve(formula1)
    print(f"Solution: {solution1}")
    
    # Example 2: DPLL solver
    print("\n2. DPLL Solver:")
    print("-" * 60)
    
    solver_dpll = DPLL()
    solution2 = solver_dpll.solve(formula1)
    print(f"Solution: {solution2}")
    print(f"Recursive calls: {solver_dpll.call_count}")
    
    # Example 3: Graph coloring
    print("\n3. Graph 3-Coloring Problem:")
    print("-" * 60)
    
    # Simple triangle graph: 0-1-2-0
    edges = [(0, 1), (1, 2), (2, 0)]
    coloring = ThreeColorability.solve_coloring(edges, 3)
    
    if coloring:
        print("Valid 3-coloring found:")
        for i in range(3):
            for c in range(3):
                if coloring.get(f"c{i}_{c}", False):
                    colors = {0: "Red", 1: "Green", 2: "Blue"}
                    print(f"  Node {i}: {colors[c]}")
    else:
        print("No valid 3-coloring found")
