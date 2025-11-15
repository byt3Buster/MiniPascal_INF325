class Parser:
    def __init__(self, tokens):
        """
        reçois en paramètre les tokens issues de lexer
        commence à analyser le premier token
        """
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]

    def move(self):
        """
        déplace d'un pas dans la liste des tokens
        """
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]

    def parse(self):
        """
        Lance le parsing complet à partir du plus haut niveau de la
        grammaire (expression).

        Retourne un liste imbriquée representant l'arbre binaire
        """
        return self.expression()
    
    def factor(self):
        """
        Si le token encours est du type INT ou FLOAT
        Retourner
        """
        token = self.token
        if token.type in ("INT", "FLOAT"):
            return self.token
    
    def term(self):
        """
        Lit le premier facteur à gauche
        Avance d'un pas
        Tantque le prochain token est soit * ou /, on memorise dans operation
            Avance d'un pas
            Lit le facteur droite
            Crée un noeud binaire avec operation comme racine
        """
        left_node = self.factor()
        self.move()
        while self.token.value in ("*", "/"):
            operation = self.token
            self.move()
            right_node = self.factor()
            self.move()
            left_node = [left_node, operation, right_node]
        
        return left_node

    def expression(self):
        """
        Lit le premier term à gauche
        Pas besoin d'avancer d'un pas puisque on avance d'un pas dans term
        Tantque le prochain token est soit - ou +, on memorise dans operation
            Avance d'un pas
            Lit le term droite
            Crée un noeud binaire avec operation comme racine
        Retourne l'arbre binaire final
        """
        left_node = self.term()
        while self.token.value in ("+", "-"):
            operation = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operation, right_node]

        return left_node