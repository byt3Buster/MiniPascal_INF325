from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
"""
Shell interactif pour les tests
"""

while True:
    """
    > 1 + 1
    Tokens -> [1, +, 1] 
    BTree -> [1, +, 1]
    Result -> 2
    """
    exp = input("> ")
    tokenizer = Lexer(exp)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter(tree)
    result = interpreter.interpret()

    print(f"Tokens -> {tokens} \nBTree -> {tree}\nResult -> {result}")