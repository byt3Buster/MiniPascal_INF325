class Token:
    """
    Toute les élément d'une expression héritent de Token
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        """
        Utile pour soigner l'affichage d'un objet
        Une autre façon de representer l'objet quoi!
        """
        return str(self.value)

class Integer(Token):
    def __init__(self, value):
        super().__init__("INT", value)

class Float(Token):
    def __init__(self, value):
        super().__init__("FLOAT", value)

class Operation(Token):
    def __init__(self, value):
        super().__init__("OP", value)

class Declaration(Token):
    def __init__(self, value):
        super().__init__("DECL", value)

class Variable(Token):
    def __init__(self, value):
        super().__init__("VAR", value)