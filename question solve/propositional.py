from logic import LogicalEngine


def solve_propositional_questions():
    engine = LogicalEngine()

    questions = [
        (
            "a",
            "It is raining outside if and only if it is a cloudy day.",
            "p IFF q",
            {"p": "It is raining outside", "q": "It is a cloudy day"},
        ),
        (
            "b",
            "If you get a 100 on the final exam, then you earn an A in the class.",
            "p -> q",
            {"p": "You get 100 on final exam", "q": "You earn an A"},
        ),
        (
            "d",
            "She studied hard or she is extremely bright.",
            "p OR q",
            {"p": "She studied hard", "q": "She is extremely bright"},
        ),
        (
            "e",
            "I am a rock and I am an island.",
            "p AND q",
            {"p": "I am a rock", "q": "I am an island"},
        ),
    ]

    for tag, sentence, symbolic, mapping in questions:
        print(f"\nQuestion {tag}: {sentence}")
        print(f"Symbolic form: {symbolic}")
        for var, meaning in mapping.items():
            print(f"  {var} = {meaning}")
        engine.generate_truth_table(symbolic, f"Propositional Question {tag}")


if __name__ == "__main__":
    solve_propositional_questions()
