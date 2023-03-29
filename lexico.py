# -*- coding: utf-8 -*-


print("")

# Cimplificado
# Usando a ferramenta py.lex

import ply.lex as lex

tokens = (
   'ID', # identificador
   'NUMBER', # constantes numéricas   
   'PLUS', # +
   'MINUS', # -
   'TIMES', # *
   'DIVIDE', # /
   'EQUALS', # declarar
   'LESS_THAN',
   'LESS_THAN_EQUAL', 
   'GREATER_THAN',
   'GREATER_THAN_EQUAL',
   'AND',
   'OR',
   'NOT'
)

t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER= r'\d+' 
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_THAN_EQUAL = r'<='
t_GREATER_THAN_EQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# Ignora espaço e quebra de linha
t_ignore = ' \t\n'

def t_error(t): 
    print("Cabou-se, deu erro em", t)
    t.lexer.skip(1) 
lexer = lex.lex() 





def testes():
    # Declarar variavel 
    data = "aaaaa = 1" 
    lexer.input(data) 
    print(lexer.token())


    for tok in lexer:
        print(tok.type)


testes()