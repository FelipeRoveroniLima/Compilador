# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 14:46:48 2023

@author: sergi
"""
import ply.lex as lex
import ply.yacc as yacc

from lexico import Lexico

class Parser:
    def __init__(self):
        self.lexico = Lexico()
        self.tokens = self.lexico.tokens
        self.parser = yacc.yacc(module=self)
        
    def p_statement_assign(self, p):
        'statement : ID EQUALS expr SEMICOLON'
    
    def p_expr_binop(self, p):
        '''expr : expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr'''
    
    def p_expr_relational(self, p):
        '''expr : expr LESS_THAN expr
                | expr LESS_THAN_EQUAL expr
                | expr GREATER_THAN expr
                | expr GREATER_THAN_EQUAL expr'''
    
    def p_expr_logical(self, p):
        '''expr : expr AND expr
                | expr OR expr
                | NOT expr'''
    
    def p_expr_group(self, p):
        'expr : LEFT_PAREN expr RIGHT_PAREN'
    
    def p_expr_id(self, p):
        'expr : ID'
    
    def p_expr_num(self, p):
        'expr : NUMBER'
    
    def p_error(self, p):
        print("Syntax error in input!")
        
    def testes(self, texto):
        return self.parser.parse(texto, lexer=self.lexico.lexico)
p = Parser()
result = p.parser.parse("x = 3 + 4;", lexer=p.lexico.lexico)
print(result)