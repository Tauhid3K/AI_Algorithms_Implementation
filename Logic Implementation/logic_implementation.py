"""
Logic Implementation
Implements logic gates + Boolean expression analyzer using truth tables.
"""

from typing import List, Dict, Tuple
import re
from itertools import product


# =========================
# Logic Gates
# =========================

class LogicGate:
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, *inputs: bool) -> bool:
        raise NotImplementedError


class ANDGate(LogicGate):
    def __init__(self):
        super().__init__("AND")

    def evaluate(self, *inputs: bool) -> bool:
        return all(inputs)


class ORGate(LogicGate):
    def __init__(self):
        super().__init__("OR")

    def evaluate(self, *inputs: bool) -> bool:
        return any(inputs)


class NOTGate(LogicGate):
    def __init__(self):
        super().__init__("NOT")

    def evaluate(self, *inputs: bool) -> bool:
        if len(inputs) != 1:
            raise ValueError("NOT gate needs exactly 1 input")
        return not inputs[0]


class XORGate(LogicGate):
    def __init__(self):
        super().__init__("XOR")

    def evaluate(self, *inputs: bool) -> bool:
        if len(inputs) != 2:
            raise ValueError("XOR gate needs exactly 2 inputs")
        return inputs[0] != inputs[1]


# =========================
# Boolean Expression Engine
# =========================

class BooleanExpression:
    def __init__(self, expression: str):
        self.expression = expression
        self.variables = self._extract_variables()

    def _extract_variables(self):
        return set(re.findall(r'\b[A-Z]\b', self.expression))

    def evaluate(self, **values: bool) -> bool:
        expr = self.expression

        # replace variables with values
        for var in self.variables:
            expr = re.sub(rf'\b{var}\b', str(values[var]), expr)

        # replace operators
        expr = expr.replace("AND", "and")
        expr = expr.replace("OR", "or")
        expr = expr.replace("NOT", "not")

        return bool(eval(expr, {"__builtins__": None}, {}))

    def truth_table(self) -> List[Dict]:
        vars_sorted = sorted(self.variables)
        table = []

        for values in product([False, True], repeat=len(vars_sorted)):
            var_dict = dict(zip(vars_sorted, values))
            result = self.evaluate(**var_dict)
            table.append({**var_dict, "Result": result})

        return table

    def print_truth_table(self):
        table = self.truth_table()

        if not table:
            print("No variables found.")
            return

        cols = sorted(self.variables) + ["Result"]
        width = 6

        # header
        header = " | ".join(f"{c:^{width}}" for c in cols)
        print(header)
        print("-" * len(header))

        # rows
        for row in table:
            values = [str(int(row[c])) for c in cols]
            print(" | ".join(f"{v:^{width}}" for v in values))


# =========================
# Analyzer (CORE PART)
# =========================

class TruthTableAnalyzer:

    @staticmethod
    def is_tautology(expr: BooleanExpression) -> bool:
        return all(row["Result"] for row in expr.truth_table())

    @staticmethod
    def is_contradiction(expr: BooleanExpression) -> bool:
        return not any(row["Result"] for row in expr.truth_table())

    @staticmethod
    def is_contingency(expr: BooleanExpression) -> bool:
        return not (
            TruthTableAnalyzer.is_tautology(expr) or
            TruthTableAnalyzer.is_contradiction(expr)
        )

    @staticmethod
    def are_equivalent(expr1: BooleanExpression, expr2: BooleanExpression) -> bool:
        all_vars = sorted(expr1.variables | expr2.variables)

        for values in product([False, True], repeat=len(all_vars)):
            var_dict = dict(zip(all_vars, values))

            r1 = expr1.evaluate(**{v: var_dict[v] for v in expr1.variables})
            r2 = expr2.evaluate(**{v: var_dict[v] for v in expr2.variables})

            if r1 != r2:
                return False

        return True


# =========================
# MAIN PROGRAM
# =========================

if __name__ == "__main__":

    print("=== LOGIC GATES ===")

    and_gate = ANDGate()
    or_gate = ORGate()
    not_gate = NOTGate()
    xor_gate = XORGate()

    print("AND(True, True) =", int(and_gate.evaluate(True, True)))
    print("OR(True, False) =", int(or_gate.evaluate(True, False)))
    print("NOT(True) =", int(not_gate.evaluate(True)))
    print("XOR(True, False) =", int(xor_gate.evaluate(True, False)))

    print("\n=== BOOLEAN EXPRESSION ===")

    expr = BooleanExpression("(A AND B) OR (NOT C)")
    print("Expression:", expr.expression)
    expr.print_truth_table()

    print("\n=== ANALYSIS (BASED ON SAME EXPRESSION) ===")

    print("Tautology:",
          "YES" if TruthTableAnalyzer.is_tautology(expr) else "NO")

    print("Contradiction:",
          "YES" if TruthTableAnalyzer.is_contradiction(expr) else "NO")

    print("Contingency:",
          "YES" if TruthTableAnalyzer.is_contingency(expr) else "NO")
