class Parser:
    def __init__(self, tokens):
        """
        Reçoit en paramètre les tokens issus du lexer
        Commence à analyser le premier token
        """
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx] if self.tokens else None

    def move(self):
        """Déplace d'un pas dans la liste des tokens"""
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
        else:
            self.token = None

    # -----------------------------
    # Expressions et termes
    # -----------------------------
    def factor(self):
        """
        Un facteur est une élément entier ou flottant
        Gestion des priorités dans les parenthèses
        """
        token = self.token
        if token is None:
            return None

        if token.type in ("INT", "FLOAT"):
            node = token
            self.move()
            return node

        elif token.value == "(":
            """
            Si on rencontre une parenthèse, extraire l'expression et
            continuer
            """
            self.move()
            expr = self.expression()
            if self.token.value == ")":
                self.move()
            return expr

        elif token.type.startswith("VAR"):
            node = token
            self.move()
            return node

    def term(self):
        """
        Un termes est multiplication de 2 ou plusieurs facteurs
        """
        left_node = self.factor()
        while self.token is not None and self.token.value in ("*", "/"):
            op = self.token
            self.move()
            right_node = self.factor()
            left_node = [left_node, op, right_node]
        return left_node

    def expression(self):
        """
        Une expression est l'addition de deux ou plusieurs terme
        """
        left_node = self.term()
        while self.token is not None and self.token.value in ("+", "-"):
            op = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, op, right_node]
        return left_node

    # -----------------------------
    # Variable
    # -----------------------------
    def variable(self):
        if self.token is not None and self.token.type.startswith("VAR"):
            node = self.token
            self.move()
            return node

    # -----------------------------
    # Statement
    # -----------------------------
    def statement(self):
        """
        Reconnaît les statements :
        - déclaration de variable avec := (affectation)
        - expression seule
        """
        if self.token is None:
            return None

        # Déclaration ou affectation
        if self.token.type == "KEYWORD":
            keyword_token = self.token
            self.move()

            # Exemple : var x : integer
            if keyword_token.value == "var":
                var_token = self.variable()
                # on peut vérifier le type suivant ': TYPE'
                if self.token and self.token.value == ":":
                    self.move()
                    type_token = self.token
                    self.move()
                    return [keyword_token, var_token, type_token]

            # Exemple : affectation x := expression
            elif keyword_token.value in ("program", "begin", "end"):
                # Pour l'instant on les retourne seuls
                return keyword_token

        # Affectation classique : VAR := expression
        if self.token.type.startswith("VAR"):
            left_node = self.variable()
            if self.token and self.token.value == ":=":
                op = self.token
                self.move()
                right_node = self.expression()
                return [left_node, op, right_node]

        # Sinon expression simple
        return self.expression()

    # -----------------------------
    # Parser complet
    # -----------------------------
    def parse(self):
        """
        Parse tous les tokens et renvoie une liste de statements
        """
        statements = []
        while self.token is not None:
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            # Ignore les ';' séparateurs
            if self.token and self.token.value == ";":
                self.move()
        return statements