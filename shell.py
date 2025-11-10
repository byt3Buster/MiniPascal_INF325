from lexer import Lexer

"""
Shell interactif pour les tests
"""

while True:
    """
    > 1 + 1
    [1, +, 1]
    """
    exp = input("> ")
    tokenizer = Lexer(exp)
    tokens = tokenizer.tokenize()

    print(tokens)