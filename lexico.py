# -*- coding: utf-8 -*-


print("aaaaa")

# Ideia inicial, fazer igualzinho C
# Usando a ferramenta py.lex

import ply.lex as lex

tokens = (
   'ID', # identificador
   'NUMBER', # constantes numéricas
   'OP', # operadores
   
)

t_ID = r'[a-zA-Z_]'
t_NUMBER = r'[0-9]'
t_OP = r'[+,-]'

def t_error(t): 
    print("Cabou-se ")
    t.lexer.skip(1) 
lexer = lex.lex() 


