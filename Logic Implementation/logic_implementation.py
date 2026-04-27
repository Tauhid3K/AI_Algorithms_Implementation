"""
Logic Implementation
Implements basic logic gates and Boolean operations.
"""

from typing import Union, List, Dict, Tuple
from enum import Enum


class LogicGate:
    """Base class for logic gates."""
    
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, *inputs: bool) -> bool:
        """Evaluate the logic gate with given inputs."""
        raise NotImplementedError


class ANDGate(LogicGate):
    """AND Logic Gate - outputs True only if all inputs are True."""
    
    def __init__(self):
        super().__init__("AND")
    
    def evaluate(self, *inputs: bool) -> bool:
        """
        AND gate logic.
        
        Args:
            *inputs: Variable number of boolean inputs
            
        Returns:
            True if all inputs are True, False otherwise
        """
        return all(inputs)


class ORGate(LogicGate):
    """OR Logic Gate - outputs True if at least one input is True."""
    
    def __init__(self):
        super().__init__("OR")
    
    def evaluate(self, *inputs: bool) -> bool:
        """
        OR gate logic.
        
        Args:
            *inputs: Variable number of boolean inputs
            
        Returns:
            True if at least one input is True, False otherwise
        """
        return any(inputs)


class NOTGate(LogicGate):
    """NOT Logic Gate - inverts the input."""
    
    def __init__(self):
        super().__init__("NOT")
    
    def evaluate(self, *inputs: bool) -> bool:
        """
        NOT gate logic.
        
        Args:
            *inputs: Single boolean input
            
        Returns:
            Inverted input
        """
        if len(inputs) != 1:
            raise ValueError("NOT gate requires exactly one input")
        return not inputs[0]


class NANDGate(LogicGate):
    """NAND Logic Gate - negation of AND."""
    
    def __init__(self):
        super().__init__("NAND")
    
    def evaluate(self, *inputs: bool) -> bool:
        """NAND gate logic."""
        return not all(inputs)


class NORGate(LogicGate):
    """NOR Logic Gate - negation of OR."""
    
    def __init__(self):
        super().__init__("NOR")
    
    def evaluate(self, *inputs: bool) -> bool:
        """NOR gate logic."""
        return not any(inputs)


class XORGate(LogicGate):
    """XOR Logic Gate - outputs True if inputs are different."""
    
    def __init__(self):
        super().__init__("XOR")
    
    def evaluate(self, *inputs: bool) -> bool:
        """
        XOR gate logic.
        
        Args:
            *inputs: Two boolean inputs
            
        Returns:
            True if inputs are different, False if they're the same
        """
        if len(inputs) != 2:
            raise ValueError("XOR gate requires exactly two inputs")
        return inputs[0] != inputs[1]


class XNORGate(LogicGate):
    """XNOR Logic Gate - negation of XOR."""
    
    def __init__(self):
        super().__init__("XNOR")
    
    def evaluate(self, *inputs: bool) -> bool:
        """XNOR gate logic."""
        if len(inputs) != 2:
            raise ValueError("XNOR gate requires exactly two inputs")
        return inputs[0] == inputs[1]


class BooleanExpression:
    """Represents and evaluates Boolean expressions."""
    
    def __init__(self, expression: str):
        """
        Initialize Boolean expression.
        
        Args:
            expression: Expression string with variables (A, B, C, etc.) and operators (AND, OR, NOT, ^, |, ~)
        """
        self.expression = expression
        self.variables = self._extract_variables()
    
    def _extract_variables(self) -> set:
        """Extract variable names from expression."""
        import re
        # Find all uppercase letters as variables
        return set(re.findall(r'[A-Z]', self.expression))
    
    def evaluate(self, **variable_values: bool) -> bool:
        """
        Evaluate the Boolean expression.
        
        Args:
            **variable_values: Dictionary mapping variable names to boolean values
            
        Returns:
            Result of evaluating the expression
        """
        # Replace variables with their values
        expr = self.expression
        for var in self.variables:
            if var not in variable_values:
                raise ValueError(f"Missing value for variable {var}")
            expr = expr.replace(var, str(variable_values[var]))
        
        # Replace operators
        expr = expr.replace("AND", "and")
        expr = expr.replace("OR", "or")
        expr = expr.replace("NOT", "not")
        expr = expr.replace("^", "and")
        expr = expr.replace("|", "or")
        expr = expr.replace("~", "not ")
        
        # Evaluate
        return bool(eval(expr))
    
    def truth_table(self) -> List[Dict]:
        """
        Generate truth table for the expression.
        
        Returns:
            List of dictionaries showing all possible combinations and results
        """
        from itertools import product
        
        table = []
        num_vars = len(self.variables)
        
        for values in product([False, True], repeat=num_vars):
            var_dict = dict(zip(sorted(self.variables), values))
            result = self.evaluate(**var_dict)
            row = {**var_dict, "Result": result}
            table.append(row)
        
        return table
    
    def print_truth_table(self):
        """Print truth table in a formatted way."""
        table = self.truth_table()
        
        if not table:
            return
        
        # Get column names
        columns = sorted(self.variables) + ["Result"]
        
        # Print header
        print(" | ".join(columns))
        print("-" * (len(columns) * 8))
        
        # Print rows
        for row in table:
            values = [str(row[col]) for col in columns]
            print(" | ".join(f"{v:^6}" for v in values))


class TruthTableAnalyzer:
    """Analyzes Boolean expressions using truth tables."""
    
    @staticmethod
    def is_tautology(expression: BooleanExpression) -> bool:
        """
        Check if expression is a tautology (always True).
        
        Args:
            expression: BooleanExpression to check
            
        Returns:
            True if expression is a tautology
        """
        table = expression.truth_table()
        return all(row["Result"] for row in table)
    
    @staticmethod
    def is_contradiction(expression: BooleanExpression) -> bool:
        """
        Check if expression is a contradiction (always False).
        
        Args:
            expression: BooleanExpression to check
            
        Returns:
            True if expression is a contradiction
        """
        table = expression.truth_table()
        return not any(row["Result"] for row in table)
    
    @staticmethod
    def is_contingency(expression: BooleanExpression) -> bool:
        """
        Check if expression is a contingency (sometimes True, sometimes False).
        
        Args:
            expression: BooleanExpression to check
            
        Returns:
            True if expression is a contingency
        """
        return not (TruthTableAnalyzer.is_tautology(expression) or 
                   TruthTableAnalyzer.is_contradiction(expression))
    
    @staticmethod
    def are_equivalent(expr1: BooleanExpression, expr2: BooleanExpression) -> bool:
        """
        Check if two Boolean expressions are logically equivalent.
        
        Args:
            expr1: First expression
            expr2: Second expression
            
        Returns:
            True if expressions are equivalent
        """
        all_vars = sorted(expr1.variables | expr2.variables)
        
        if len(all_vars) > 20:  # Limit for computational efficiency
            print("Too many variables for truth table comparison")
            return False
        
        from itertools import product
        
        for values in product([False, True], repeat=len(all_vars)):
            var_dict = dict(zip(all_vars, values))
            result1 = expr1.evaluate(**{v: var_dict[v] for v in expr1.variables})
            result2 = expr2.evaluate(**{v: var_dict[v] for v in expr2.variables})
            
            if result1 != result2:
                return False
        
        return True
    
    @staticmethod
    def demorgan_first_law(a: bool, b: bool) -> Tuple[bool, bool]:
        """
        De Morgan's First Law: NOT(A AND B) = (NOT A) OR (NOT B)
        """
        left = not (a and b)
        right = (not a) or (not b)
        return left, right
    
    @staticmethod
    def demorgan_second_law(a: bool, b: bool) -> Tuple[bool, bool]:
        """
        De Morgan's Second Law: NOT(A OR B) = (NOT A) AND (NOT B)
        """
        left = not (a or b)
        right = (not a) and (not b)
        return left, right


# Example usage and tests
if __name__ == "__main__":
    print("=== Logic Gates ===")
    
    # Test individual gates
    and_gate = ANDGate()
    or_gate = ORGate()
    not_gate = NOTGate()
    xor_gate = XORGate()
    
    print(f"AND(True, True) = {and_gate.evaluate(True, True)}")
    print(f"AND(True, False) = {and_gate.evaluate(True, False)}")
    print(f"OR(True, False) = {or_gate.evaluate(True, False)}")
    print(f"NOT(True) = {not_gate.evaluate(True)}")
    print(f"XOR(True, False) = {xor_gate.evaluate(True, False)}")
    
    print("\n=== Boolean Expression ===")
    
    # Test Boolean expression
    expr = BooleanExpression("A AND B OR NOT C")
    print(f"\nExpression: A AND B OR NOT C")
    expr.print_truth_table()
    
    print("\n=== Truth Table Analysis ===")
    
    # Test tautology
    tautology_expr = BooleanExpression("A OR NOT A")
    print(f"\n'{tautology_expr.expression}' is tautology: {TruthTableAnalyzer.is_tautology(tautology_expr)}")
    
    # Test contradiction
    contradiction_expr = BooleanExpression("A AND NOT A")
    print(f"'{contradiction_expr.expression}' is contradiction: {TruthTableAnalyzer.is_contradiction(contradiction_expr)}")
    
    # Test equivalence
    expr1 = BooleanExpression("A OR B")
    expr2 = BooleanExpression("B OR A")
    print(f"\n'{expr1.expression}' equivalent to '{expr2.expression}': {TruthTableAnalyzer.are_equivalent(expr1, expr2)}")
