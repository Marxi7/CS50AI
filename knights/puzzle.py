from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is  either a Knight or a Knave but not both at the same time as the rules mentionned.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # If A is a Knave, him being a Knight and a Knave is False
    Implication(AKnave, Not(And(AKnight, AKnave))),
    # If A is a Knight, him being a Knight and a Knave is True
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A or B are either Knight or Knave, but not both at the same time as the rules mentionned.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # If A is knight, A & B are both Knaves.
    Implication(AKnight, And(AKnave, BKnave)),
    #If A is a Knave, A & B are both NOT Knaves.
    Implication(AKnave, Not(And(AKnave, BKnave))),

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
     # A or B are either Knight or Knave, but not both at the same time as the rules mentionned.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # If a is a knight, either A and B are knight or A and B are Knaves.
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If a is a Knave, either Not A and B are knight or A and B are Knaves.
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a Knight, A and B are not the same kinds.
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a Knave, A & B are the same kinds.
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
     # A, B or C are either Knight or Knave, but not both at the same time as the rules mentionned.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),


    # FROM WHAT A SAYS :

    # If A is a Knight, either A 'Being a Knight' or A 'Being a Knave is True
    Implication(AKnight, Or(AKnight, AKnave)),
    # But if A is a Knave, either A 'Being a Knight' or A 'being a Knave' is False
    Implication(AKnave, Not(Or(AKnight, AKnave))),


    # FROM WHAT B SAYS

    # If B is a Knight, then C is a Knave
    Implication(BKnight, CKnave),
    # If B is a Knave, C is not a Knave
    Implication(BKnave, Not(CKnave)),

    Or(
        Implication(BKnight, 
            Or( 
                # If B is a Knight and A is Knight, then A told the truth about being a Knave to B
                Implication(AKnight, AKnave),
                # But even if B is a Knight, A could be a Knave, and therefore, lie about being a Knave to B
                Implication(AKnave, Not(AKnave))
            )
        ),

        Implication(BKnave,
            Not(
                Or(
                    # If B is a Knave, then even if A is a Knight, what A says to be is Not true as B lies about what A says.
                    Implication(AKnight, AKnave),
                    # Same for the 'lies' A being a Knave could tell to B. If B is a Knave, he would Lie about the lies he heard from A.
                    Implication(AKnave, Not(AKnave))
                )
            )
        )
    ),


    # FROM WHAT C SAYS:

    # If C is a Knight, A is a Knight
    Implication(CKnight, AKnight),
    # If C is a Knave, A is Not a Knight
    Implication(CKnave, Not(AKnight)),
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
