from logic import PropositionalLogicEngine


def run_logic_demo():
    engine = PropositionalLogicEngine()

    print("=== LOGIC DEMO (EXAM STYLE) ===")

    engine.generate_truth_table(
        "(p -> q) AND (q -> r) -> (p -> r)",
        "Input example with mixed operators/symbols",
    )

    engine.generate_truth_table("p OR NOT p", "Known tautology")
    engine.generate_truth_table("p AND NOT p", "Known contradiction")


if __name__ == "__main__":
    run_logic_demo()
