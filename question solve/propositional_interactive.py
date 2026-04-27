from logic import PropositionalLogicEngine


def run_propositional_interactive():
    engine = PropositionalLogicEngine()

    print("=== PROPOSITIONAL INTERACTIVE MODE ===")
    print("Enter sentence label + symbolic expression.")
    print("Example symbolic forms: p IFF q, p -> q, p OR q, p AND q")
    print("Type 'exit' as sentence to stop.\n")

    while True:
        sentence = input("Natural language sentence: ").strip()
        if sentence.lower() in {"exit", "quit"}:
            print("Exiting interactive mode.")
            break
        if not sentence:
            print("Please enter a sentence.\n")
            continue

        symbolic = input("Symbolic expression: ").strip()
        if not symbolic:
            print("Please enter a symbolic expression.\n")
            continue

        print(f"Sentence: {sentence}")
        print(f"Symbolic: {symbolic}")
        try:
            engine.generate_truth_table(symbolic, "User input propositional expression")
        except Exception as err:
            print(f"Error: {err}")
        print()


if __name__ == "__main__":
    run_propositional_interactive()
