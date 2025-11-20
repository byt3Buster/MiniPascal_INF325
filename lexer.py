"""
Analyse lexicale d'un fichier source pascal
"""
from tokens import Integer, Float, Operation, Keyword, Variable, Token

class Lexer:
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    stopwords = [" ", "\n", "\t"] # caractères à ignorer

    # mots-clés Pascal simplifiés
    keywords = ["program", "var", "begin", "end"]
    types = ["integer", "float"]

    # opérateurs simples
    operations = "+-*/();:"

    def __init__(self, source: str):
        """
        Récupération du string source

        """
        self.source = source
        self.idx = 0
        self.tokens = []
        self.char = self.source[self.idx] if self.source else None
        self.token = None

    # -----------------------------
    # Avancer dans le texte
    # -----------------------------
    def move(self, n=1):
        """
        Passer au caractère suivant à condition que son idx ne dépasse
        pas la taille de l'expression
        """
        self.idx += n
        if self.idx < len(self.source):
            self.char = self.source[self.idx]
        else:
            self.char = None

    # -----------------------------
    # Vérifier correspondance
    # -----------------------------
    def match(self, text):
        """
        Vérifie si la prochaine chaîne dans source
        correspond à text
        """
        return self.source[self.idx:self.idx + len(text)] == text

    # -----------------------------
    # Tokenisation principale
    # -----------------------------
    def tokenize(self):
        """
        tokenization de self.exp
        Retourne tout les tokens reconnaissable trouvés dans exp
        """
        while self.char is not None:
            """
            -> Si les 2 prochain char correspondent à l'opérateur d'affectation
               :=, créer le token et avancer de 2 pas
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
            # ignorer les espaces
            if self.char in Lexer.stopwords:
                self.move()
                continue

            # opérateur multi-caractères := doit venir avant le reste
            if self.match(":="):
                self.tokens.append(Operation(":="))
                self.move(2)
                continue

            # extraction des nombres
            if self.char in Lexer.digits:
                self.tokens.append(self.extract_number())
                continue

            # extraction des mots
            if self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.keywords:
                    self.tokens.append(Keyword(word))

                elif word in Lexer.types:
                    self.tokens.append(Token("TYPE", word))

                else:
                    self.tokens.append(Variable(word))

                continue

            # opérateurs simples
            if self.char in Lexer.operations:
                self.tokens.append(Operation(self.char))
                self.move()
                continue

            # caractère inconnu
            raise Exception(f"Caractère non reconnu: {self.char}")

        return self.tokens

    # -----------------------------
    # Extraction d'un nombre
    # -----------------------------
    def extract_number(self):
        """
        Extrait tantque le prochain caractère est un chiffre
        ou un . et l'idx du caractère encours est inférieur à la taille de exp

        Si un . est trouvé, number devient un Float

        Ajouter le digit ou le . et passer au caractère suivant
        """
        number = ""
        is_float = False

        while self.char is not None and (self.char in Lexer.digits or self.char == "."):
            if self.char == ".":
                is_float = True
            number += self.char
            self.move()

        return Float(number) if is_float else Integer(number)

    # -----------------------------
    # Extraction d'un mot
    # -----------------------------
    def extract_word(self):
        """
        Extrait tantque le caractère encours est une lettre
        Et l'index ne dépasse pas la taille de l'expression

        Retourne le mot extrait à la fin
        """
        word = ""
        while self.char is not None and self.char in Lexer.letters:
            word += self.char
            self.move()
        return word