# -*- coding: utf-8 -*-



# Cimplificado
# Usando a ferramenta py.lex

import ply.lex as lex
import ply.yacc as yacc

class Lexico:
    tokens = [
       'ID', # identificador
       'NUMBER', # constantes numéricas   
       'STRING', # caracteres
       'PLUS', # +
       'MINUS', # -
       'TIMES', # *
       'DIVIDE', # /
       'EQUALS', # declarar
       'LESS_THAN',
       'LESS_THAN_EQUAL', 
       'GREATER_THAN',
       'GREATER_THAN_EQUAL',
       'AND', # &&
       'OR', # ||
       'NOT', # !
       'RIGHT_PAREN', # )
       'LEFT_PAREN', # (
       'RIGHT_BRACE', # }
       'LEFT_BRACE', # {
       'RIGHT_BRACKET', # ]
       'LEFT_BRACKET', # [
       'COMMA', # ,
       'SEMICOLON' # ;
       
    ]
    
    reserved = {
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'while': 'WHILE',
        'print': 'PRINT',
        'true' : 'TRUE',
        'false' : 'FALSE',
    }
    tokens += list(reserved.values())
    
    
    #t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_NUMBER = r'\d+(\.\d+)?' 
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
    t_RIGHT_PAREN = r'\)'
    t_LEFT_PAREN = r'\('
    t_RIGHT_BRACE = r'\}'
    t_LEFT_BRACE = r'\{'
    t_RIGHT_BRACKET = r'\]'
    t_LEFT_BRACKET = r'\['
    t_COMMA = r','
    t_SEMICOLON = r';'
    # Ignora espaço e quebra de linha
    t_ignore = ' \t\n'
    
    def __init__(self):
        self.lexico = lex.lex(module=self)
    
    def t_STRING(self, t):
        r'"([^\\\n]|(\\.))*?"'
        t.value = t.value[1:-1] 
        return t
    
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t
    
    
    def t_error(self, t): 
        print("Cabou-se, deu erro em", t)
        t.lexer.skip(1) 
    
    
    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = int(p[1])
        
    def p_error(self, p):
        print("Errou '%s'" % p.value)
        

    
    def testes_lex(self):
        lexer = lex.lex()     
        # Declarar variavel 
        data = "aaaaa" 
        lexer.input(data) 
        tokens = [tok.type for tok in lexer]
        assert tokens == ['ID']
        
        data = "1"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['NUMBER']
        
        data = '"asdawdadwad"'
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['STRING']   
        
        data = "+"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['PLUS']
    
        data = "*"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['TIMES']    
        
        data = "-"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['MINUS']        
        
        data = "/"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['DIVIDE']        
    
        data = "="
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['EQUALS']
               
        data = "<"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['LESS_THAN']
    
        data = ">"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['GREATER_THAN']
    
        data = "<="
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['LESS_THAN_EQUAL']
    
        data = ">="
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['GREATER_THAN_EQUAL']
    
        data = "&&"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['AND']
    
        data = "||"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['OR']
    
        data = "!"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['NOT']
    
        data = "("
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['LEFT_PAREN']
    
        data = ")"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['RIGHT_PAREN']
    
        data = "{"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['LEFT_BRACE']
    
        data = "}"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['RIGHT_BRACE']
    
        data = "["
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['LEFT_BRACKET']
    
        data = "]"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['RIGHT_BRACKET']
    
        data = ","
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['COMMA']
    
        data = ";"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['SEMICOLON']
    
        data = "if"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['IF']
    
        data = "then"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['THEN']
    
        data = "while"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['WHILE']
    
        data = "print"
        lexer.input(data)
        tokens = [tok.type for tok in lexer]
        assert tokens == ['PRINT']

#aa = Lexico()
#aa.testes_lex