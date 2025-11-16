"""
Analyse lexicale d'une expression
"""
from tokens import Integer, Float, Operation, Declaration, Variable

class Lexer:
    """
    Attribut de classe:
    - digits (chiffres possible dans une expression)
    - operations (operateurs possible)
    - stopwords (caractères ignorés)
    """
    digits = "0123456789"
    letters = "abcdefghijklmopqrstuvwxyz"
    operations = "+-/*()="
    stopwords = [" "]
    declarations = ["make"]

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
            -> Sinon so c'est une lettre, extraire le mot entier
                le mot peut être le mot clé de déclaration ou le non de la variable

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
            elif self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.declarations:
                    self.token = Declaration(word)
                else:
                    self.token = Variable(word)

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

    def extract_word(self):
        """
        Extrait tantque le caractère encours est une lettre
        Et l'index ne dépasse pas la taille de l'expression

        Retourne le mot extrait à la fin
        """
        word = ""
        while self.char in Lexer.letters and self.idx < len(self.exp):
            word += self.char
            self.move()
        return word
    
    def move(self):
        """
        Passer au caractère suivant à condition que son idx ne dépasse
        pas la taille de l'expression
        """
        self.idx += 1
        if self.idx < len(self.exp):
            self.char = self.exp[self.idx]