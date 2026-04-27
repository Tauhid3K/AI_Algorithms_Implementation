from propositional_logic_engine import PropositionalLogicEngine

def solve_exercises():
    engine = PropositionalLogicEngine()
    
    # Question A: "It is raining outside if and only if it is a cloudy day."
    # P: Raining, Q: Cloudy
    engine.generate_truth_table("P <-> Q", "A: Raining IFF Cloudy")
    
    # Question B: "If you get a 100 on the final exam, then you earn an A."
    # P: Score 100, Q: Get an A
    engine.generate_truth_table("P -> Q", "B: Score 100 IMPLIES Get A")
    
    # Question D: "She studied hard or she is extremely bright."
    # P: Studied hard, Q: Extremely bright
    engine.generate_truth_table("P OR Q", "D: Studied Hard OR Bright")
    
    # Question E: "I am a rock and I am an island."
    # P: I am a rock, Q: I am an island
    engine.generate_truth_table("P AND Q", "E: Rock AND Island")

if __name__ == "__main__":
    solve_exercises()
