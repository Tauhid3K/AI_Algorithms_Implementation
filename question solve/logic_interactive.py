from logic import PropositionalLogicEngine


def run_logic_interactive():
    engine = PropositionalLogicEngine()

    print("=== LOGIC INTERACTIVE MODE ===")
    print("Enter logical expression using operators: AND, OR, NOT, ->, IFF")
    print("Examples: (p -> q) AND (q -> r) -> (p -> r), p OR NOT p")
    print("Type 'exit' to stop.\n")

    while True:
        expression = input("Expression: ").strip()
        if expression.lower() in {"exit", "quit"}:
            print("Exiting interactive mode.")
            break
        if not expression:
            print("Please enter a non-empty expression.\n")
            continue

        description = input("Optional description: ").strip()
        try:
            engine.generate_truth_table(expression, description)
        except Exception as err:
            print(f"Error: {err}")
        print()


if __name__ == "__main__":
    run_logic_interactive()
