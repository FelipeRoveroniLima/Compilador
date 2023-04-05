# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
from lexico import Lexico
import re

class Parser:
    def __init__(self):
        self.lexico = Lexico()
        self.tokens = self.lexico.tokens
        self.parser = yacc.yacc(module=self)
        
    def p_statement_assign(self, p):
        'statement : ID EQUALS expr SEMICOLON'
        p[0] = p[3]
        return p[0]
    
    def p_expr_binop(self, p):
        '''expr : expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr'''
        if (p[2] == '+'):
            p[0] = p[1] + p[3]
        elif (p[2] == '-'):
            p[0] = p[1] - p[3]
        elif (p[2] == '*'):
            p[0] = p[1] * p[3]
        else:
            p[0] = p[1] / p[3]
    
    def p_expr_relational(self, p):
        '''expr : expr LESS_THAN expr
                | expr LESS_THAN_EQUAL expr
                | expr GREATER_THAN expr
                | expr GREATER_THAN_EQUAL expr'''
        p[0] = ('COMPARE', p[2], p[1], p[3])
    
    def p_expr_logical(self, p):
        '''expr : expr AND expr
                | expr OR expr
                | NOT expr'''
        if len(p) == 4:
             # Operadores AND e OR
            p[0] = ('LOGICAL_OP', p[2], p[1], p[3])
        else:
            # Operador NOT
            p[0] = ('LOGICAL_OP', 'NOT', p[2])
    
    def p_expr_group(self, p):
        'expr : LEFT_PAREN expr RIGHT_PAREN'
        p[0] = p[2]
    
    def p_expr_id(self, p):
        'expr : ID'
        p[0] = p[1]
    
    def p_expr_num(self, p):
        'expr : NUMBER'
        # Verifica se o número é um float
        if re.match(r'^\d+\.\d+$', p[1]):
            p[0] = float(p[1])
        # Se não for float, verifica se é um int
        elif re.match(r'^\d+$', p[1]):
            p[0] = int(p[1])
        # Se não for nenhum dos dois, lança um erro de sintaxe
        else:
            raise ValueError('Invalid number syntax')
    
    def p_error(self, p):
        print("Syntax error in input!")
        
    def testes(self, texto):
        return self.parser.parse(texto, lexer=self.lexico.lexico)
    
p = Parser()
result = p.parser.parse("x = 3.5 + 4.2;", lexer=p.lexico.lexico) # 7
print()
print(result)
print()
result = p.parser.parse("x = (3 * 2) + (4 / (4-2));", lexer=p.lexico.lexico) # 10
print(result)
print()
result = p.parser.parse("x = 1 && 2;", lexer=p.lexico.lexico) # ('LOGICAL_OP', '&&', 1, 2)
print(result)
print()
result = p.parser.parse("x = 3 >= 4;", lexer=p.lexico.lexico) # ('COMPARE', '>=', 3, 4)
print(result)
print()