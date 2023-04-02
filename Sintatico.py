# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 14:46:48 2023

@author: sergi
"""
import ply.lex as lex
import ply.yacc as yacc

from lexico import Lexico

class Sintatico:
    def __init__(self):
        self.lexico = Lexico()
        self.parser = yacc.yacc(module=self)
        
        
    def p_start(p):
        """start : expression
                 | declaration"""
        p[0] = p[1]
    
    def p_declaration(p):
        'declaration : INT ID EQUALS NUM NEWLINE'
        print(f"Declarou: {p[2]} = {p[4]}")
        p[0] = p[1]