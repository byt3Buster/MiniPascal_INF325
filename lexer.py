"""
Analyse lexicale d'une expression
"""
from tokens import *

class Lexer:
    """
    Attribut de classe:
    - digits (chiffres possible dans une expression)
    - operations (operateurs possible)
    - stopwords (caractères ignorés)
    """
    digits = "0123456789"
    operations = "+-/*"
    stopwords = [" "]

    def __init__(self, exp):
        self.exp = exp
        self.idx = 0
        self.tokens = []
        self.char = self.exp[self.idx]
        self.token = None

    def tokenize(self):
        """
        tokenization de self.exp
        Retourne tout les tokens reconnaissable trouvés dans exp
        """
        while self.idx < len(self.exp):
            """
            -> Si le caractère encours est un digit, extraite tout 
               les chiffre qui suivent
            -> Sinon si c'est un opérateur, l'extraire
               et avancer d'un pas
            -> Sinon si c'est un stopwords, l'ignorer et continuer sans
               rien ajouter à tokens

            A chaque token trouvé, l'ajouter à tokens
            """
            if self.char in Lexer.digits:
                self.token = self.extract_number()
            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()
            elif self.char in Lexer.stopwords:
                self.move()
                continue

            self.tokens.append(self.token)

        return self.tokens
    
    def extract_number(self):
        """
        Extrait tantque le prochain caractère est un chiffre
        ou un . et l'idx du caractère encours est inférieur à la taille de exp

        Si un . est trouvé, number devient un Float

        Ajouter le digit ou le . et passer au caractère suivant
        """
        number = ""
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.exp)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()

        return Integer(number) if not isFloat else Float(number)

    def move(self):
        """
        Passer au caractère suivant à condition que son idx ne dépasse
        pas la taille de l'expression
        """
        self.idx += 1
        if self.idx < len(self.exp):
            self.char = self.exp[self.idx]