from tokens import Integer, Float, Variable, Token, Operation, Keyword

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.data = {}  # dictionnaire pour stocker les variables

    # -----------------------------
    # Lecture des valeurs
    # -----------------------------
    def read_token(self, token):
        """ 
        Convertit les integer et float
        Si la variable n'est pas déclaré, lever une exception
        Si val est un autre token, retourner le token
        """
        if isinstance(token, Integer):
            return int(token.value)
        elif isinstance(token, Float):
            return float(token.value)
        elif isinstance(token, Variable):
            if token.value not in self.data:
                raise Exception(f"Variable non définie : {token.value}")
            val = self.data[token.value]
            # si val est un Token
            if isinstance(val, Token):
                return self.read_token(val)
            return val
        else:
            return token

    # -----------------------------
    # Calcul binaire
    # -----------------------------
    def compute_bin(self, left, op, right):
        left_val = self.read_token(left) if not isinstance(left, list) else self.interpret_expr(left)
        right_val = self.read_token(right) if not isinstance(right, list) else self.interpret_expr(right)

        if op.value == ":=":
            # Affectation
            if not isinstance(left, Variable):
                raise Exception("La partie gauche de := doit être une variable")
            self.data[left.value] = right_val
            return right_val
        elif op.value == "+":
            return left_val + right_val
        elif op.value == "-":
            return left_val - right_val
        elif op.value == "*":
            return left_val * right_val
        elif op.value == "/":
            return left_val / right_val
        else:
            raise Exception(f"Opérateur inconnu : {op.value}")

    # -----------------------------
    # Interprétation d'une expression / affectation
    # -----------------------------
    def interpret_expr(self, expr):

        if isinstance(expr, list) and len(expr) == 3:
            return self.compute_bin(expr[0], expr[1], expr[2])
        elif isinstance(expr, Token):
            return self.read_token(expr)
        else:
            raise Exception(f"Expression invalide : {expr}")

    # -----------------------------
    # Interprétation complète de l'AST
    # -----------------------------
    def interpret(self):
        for node in self.ast:
            # On ignore program, begin, end
            if isinstance(node, Keyword) and node.value in ("program", "begin", "end"):
                continue
            # Déclaration de variable : [DECL(var), VAR, TYPE]
            if isinstance(node, list) and isinstance(node[0], Keyword) and node[0].value == "var":
                var_token = node[1]
                # Initialise à None
                self.data[var_token.value] = None
                continue

            if isinstance(node, list) and node[0].type == "KEYWORD" and node[0].value == "writeln":
                expr = node[1]
                value = self.interpret_expr(expr)
                print(value)

            # Affectation ou expression
            if isinstance(node, list):
                self.interpret_expr(node)

        return self.data