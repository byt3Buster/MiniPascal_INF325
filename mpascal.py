#!/usr/bin/env python3

import argparse
import os

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def save_tokens(tokens, filename):
    with open(filename, "w", encoding="utf8") as f:
        for tok in tokens:
            f.write(str(tok) + "\n")


def save_ast(ast, filename):
    with open(filename, "w", encoding="utf8") as f:
        f.write(str(ast))


def main():
    parser_cli = argparse.ArgumentParser(
        description="mpascal — mini compilateur pour fichiers .mpc"
    )
    parser_cli.add_argument("input", help="fichier source .mpc obligatoire")
    parser_cli.add_argument("--tokens", action="store_true", help="génère un fichier .tok")
    parser_cli.add_argument("--ast", action="store_true", help="génère un fichier .ast")
    parser_cli.add_argument("--run", action="store_true", help="exécute l'interpréteur")

    args = parser_cli.parse_args()

    # Vérification extension .mpc
    if not args.input.endswith(".mpc"):
        print("Erreur : le fichier source doit avoir l'extension .mpc")
        print("Exemple : mpascal programme.mpc --run")
        return

    # Lire le fichier source
    with open(args.input, "r", encoding="utf8") as f:
        source = f.read()

    base = os.path.splitext(args.input)[0]

    # Étape 1 : lexing
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    if args.tokens:
        tok_file = base + ".tok"
        save_tokens(tokens, tok_file)
        print(f"[OK] Fichier tokens généré : {tok_file}")

    # Si ni --ast ni --run : s'arrêter là
    if not (args.ast or args.run):
        return

    # Étape 2 : parsing
    parser = Parser(tokens)
    ast = parser.parse()

    if args.ast:
        ast_file = base + ".ast"
        save_ast(ast, ast_file)
        print(f"[OK] Fichier AST généré : {ast_file}")

    # Étape 3 : exécution
    if args.run:
        interpreter = Interpreter(ast)
        result = interpreter.interpret()
        print("=== Résultat de l'exécution ===")
        print(result)


if __name__ == "__main__":
    main()