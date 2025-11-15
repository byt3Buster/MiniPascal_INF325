from tokens import Integer, Float

class Interpreter:
    """
    Reçois l'abre binaire et procède à une analyse ascendante
    """
    def __init__(self, tree):
        self.tree = tree

    # Retour les valeurs des tokens Integer en int et Float en float
    
    def read_INT(self, value):
        return int(value)
    
    def read_FLOAT(self, value):
        return float(value)

    def compute_bin(self, left, op, right):
        """
        Récupère le type du terme de gauche et de droit

        Applique le read selon le type du terme avec comme argument la valeur du token

        Applique l'opération et retourne le resultat
        """
        left_type = left.type
        right_type = right.type

        left = getattr(self, f"read_{left_type}")(left.value)
        right = getattr(self, f"read_{right_type}")(right.value)

        if op.value == '+':
            output = left + right
        elif op.value == '-':
            output = left - right
        elif op.value == '*':
            output = left * right
        elif op.value == '/':
            output = left / right

        return Integer(output) if (left_type == "INT" and right_type == "INT") else Float(output) 

    def interpret(self, tree=None):
        """
        Analyse ascendante de l'arbre binaire
        Prend pas défaut None pour l'attribut tree
            A cause de la récursion, il faut passer un nouvelle arbre à interpret
            Car dans le shell, interpret est appellé avec un seul paramètre "self"
        """
        if tree is None:
            tree = self.tree

        """
        Récursion sur les sous-arbres
        """
        # Evalue le sous-arbre gauche
        left_node = tree[0] 
        if isinstance(left_node, list):
            left_node = self.interpret(left_node)

        # Evalue le sous-arbre droit
        right_node = tree[2]
        if isinstance(right_node, list):
            right_node = self.interpret(right_node)

        # Racine
        operator = tree[1]

        """
        Retour du résultat de l'pération
        """
        return self.compute_bin(left_node, operator, right_node)