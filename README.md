# MiniPascal
Implémentation d’un compilateur minimal pour un sous-ensemble du langage Pascal, incluant l’analyse lexicale, syntaxique et sémantique.

# Grammaire de l'expression arithmétique
expression -> term (('+'|'-') term)*
term       -> factor (('*'|'/') factor)*
factor     -> INT | FLOAT