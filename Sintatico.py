# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
from lexico import Lexico
import re
import pprint


class Parser:
    def __init__(self):
        self.lexico = Lexico()
        self.tokens = self.lexico.tokens
        self.parser = yacc.yacc(module=self)
        
    def p_program(self, p):
        '''program : ID EQUALS expr SEMICOLON program
                     | ID EQUALS function_call SEMICOLON program
                     | function_call SEMICOLON program
                     | expr program
                     | lambda
                     '''
        #print(p[:])
        #print(len(p))
        # 
        if len(p) == 6:            
            if p[5] != None:
                p[0] = [('ATRIBUITION', p[1], p[3])] + p[5]
            else: 
                p[0] = [('ATRIBUITION', p[1], p[3])] 
        # expr program
        elif len(p) == 3 :
            if p[2] != None:
                p[0] = [p[1]] + p[2] 
            else:
                p[0] = [p[1]] 
        #function call
        elif len(p) == 4:
            if p[3] != None:
                p[0] = [p[1]] + p[3] 
            else:
                p[0] = [p[1]]  
        # lamda
        else:
           p[0] = p[1]
         
        
         
    def p_program_function(self, p):
        'program : ID LEFT_PAREN parameters RIGHT_PAREN LEFT_BRACE program RIGHT_BRACE program'
        if p[8] != None:
            p[0] = [('FUNCTION', p[1], p[3], p[6])] + p[8]
        else:
            p[0] = [('FUNCTION', p[1], p[3], p[6])]

            
    def p_function_call(self, p):
        'function_call : ID LEFT_PAREN args RIGHT_PAREN'   
        p[0] = ('FUNCTION_CALL', p[1], p[3])
    
    def p_parameters(self, p):
        '''parameters : ID
                      | parameters COMMA ID'''
        if len(p) > 3:
            p[0] =  p[1] + [(p[3])]
        else:
            p[0] = [(p[1])]
            
    def p_expr_op(self, p):
        '''expr : expr PLUS term
            | expr MINUS term'''
        if (p[2] == '+'):
            p[0] = ('ADD', p[1], p[3])
        elif (p[2] == '-'):
            p[0] = ('SUB', p[1], p[3])
        

    def p_expr_term(self, p):
        'expr : term'
        p[0] = p[1]
    
    def p_term_op(self, p):
        '''term : term TIMES factor
            | term DIVIDE factor'''

        if (p[2] == '*'):
            p[0] = ('MUL', p[1], p[3])
        elif (p[2] == '/'):
            p[0] = ('DIV', p[1], p[3])

    
    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]
        
    def p_factor_num(self, p):
        'factor : NUMBER'
        if re.match(r'^\d+\.\d+$', p[1]):
            p[0] = float(p[1])
        # Se não for float, verifica se é um int
        elif re.match(r'^\d+$', p[1]):
            p[0] = int(p[1])
    
    def p_factor_id(self, p):
        'factor : ID'
        p[0] = p[1]
    
    def p_factor_expr(self, p):
        'factor : LEFT_PAREN expr RIGHT_PAREN'
        p[0] = p[2]
        
    def p_args(self, p):
        '''args : expr
                | args COMMA expr'''
        if len(p) > 2:
            p[0] = p[1] + [(p[3])]
        else:
            p[0] = [(p[1])]
    
    def p_expr_bin_op(self, p):
        '''expr : expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr'''
        if (p[2] == '+'):
            p[0] = ('ADD', p[1], p[3])
        elif (p[2] == '-'):
            p[0] = ('SUB', p[1], p[3])
        elif (p[2] == '*'):
            p[0] = ('MUL', p[1], p[3])
        else:
            p[0] = ('DIV', p[1], p[3])
    
    def p_expr_relational(self, p):
        '''expr : expr EQUALS_EQUALS expr
                | expr LESS_THAN expr
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
            raise ValueError('Erro no numero')
    
    def p_expr_string(self, p):
        'expr : STRING'
        p[0] = p[1]
        
    def p_expr_true(self, p):
        'expr : TRUE'
        p[0] = p[1]    
         
    def p_expr_false(self, p):
        'expr : FALSE'
        p[0] = p[1] 
        

                
    def p_expr_if(self, p):
        'expr : IF LEFT_PAREN expr RIGHT_PAREN LEFT_BRACE program RIGHT_BRACE'
        p[0] = ('IF', p[3], p[6])
        
    def p_expr_if_else(self, p):
        'expr : IF LEFT_PAREN expr RIGHT_PAREN LEFT_BRACE program RIGHT_BRACE ELSE LEFT_BRACE program RIGHT_BRACE'
        p[0] = ('IF_ELSE', p[3], p[6], p[10])
        
    def p_expr_while(self, p):
        'expr : WHILE LEFT_PAREN expr RIGHT_PAREN LEFT_BRACE program RIGHT_BRACE '
        p[0] = ('WHILE', p[3], p[6])

    def p_expr_printf(self, p):
        'expr : PRINTF LEFT_PAREN expr RIGHT_PAREN SEMICOLON'
        p[0] = ('PRINTF', p[3])    
        
        
    def p_lambda(self, p):
        'lambda :'
        pass
    
    def p_error(self, p):
        print("Erro de sintaxe!")

       
    def testes(self, texto):
        return self.parser.parse(texto, lexer=self.lexico.lexico)



class TreeNode:
    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []

def parse_tuple_to_tree(tup):
    if tup[0] == 'FUNCTION':
        node_type, value, children_lst = tup[0], (tup[1], tup[2]), tup[3] 
    elif tup[0] == 'ATRIBUITION':
        if isinstance(tup[2], tuple):
            node_type, value, children_lst = tup[0], tup[1], tup[2] 
        else:
            node_type, value, children_lst = tup[0],(tup[1], tup[2]), None    
    elif tup[0] == 'ADD' or tup[0] == 'SUB' or tup[0] == 'MUL' or tup[0] == 'DIV' :
        if isinstance(tup[2], tuple):
            node_type, value, children_lst = tup[0], tup[1], tup[2] 
        else:
            node_type, value, children_lst = tup[0],(tup[1], tup[2]), None
    
    elif len(tup) > 3:
        node_type, value, children_lst = tup[0], (tup[1], tup[2]), tup[3] 
    elif len(tup) == 3 and tup[0] != 'FUNCTION_CALL' :
        node_type, value, children_lst = tup[0], tup[1], tup[2] 
    else:
        node_type, value, children_lst = tup[0], tup[1], None
    node = TreeNode(node_type, value)
    
    if isinstance(children_lst, list) or isinstance(children_lst, tuple):
        if isinstance(children_lst, tuple):
            children_lst = [children_lst]
        for child_lst in children_lst:        
            child = parse_tuple_to_tree(child_lst)
            if child:
                node.children.append(child)
    return node

def print_tree(node, level=0):
    print(' ' * level * 4 + f'{node.type}: {node.value}')
    for child in node.children:
        print_tree(child, level+1)

"""
a = ('FUNCTION', 'main', ['x', 'y', 'z'], [('ATRIBUITION', 'x', 1), ('IF', ('COMPARE', '>', 'x', 1), [('PRINTF', 'aaa')]), ('ATRIBUITION', 'aaa', 'b')])
tree = parse_tuple_to_tree(a)
print_tree(tree)
print("\n\n\n")
result = p.parser.parse("x = (3 * 2) + (4 / (4-2));", lexer=p.lexico.lexico) # 10
print(result)
print()
result = p.parser.parse("x = 1 && 2;", lexer=p.lexico.lexico) # ('LOGICAL_OP', '&&', 1, 2)
print(result)
print()
result = p.parser.parse("x = 3 >= 4;", lexer=p.lexico.lexico) # ('COMPARE', '>=', 3, 4)
print(result)
print()
result = p.parser.parse("if (x > y){a = 1; b = 3;}", lexer=p.lexico.lexico) 
print(result)
print()
result = p.parser.parse("if (x > y){a = 1; b = 3;} else {a = 2;}", lexer=p.lexico.lexico) 
print(result)
print()
result = p.parser.parse("while (x > y){a = 1; b = 1; c = 2; a = a + 1;}", lexer=p.lexico.lexico) 
print(result)
print()
result = p.parser.parse("printf(\"aaa\");", lexer=p.lexico.lexico) 
print(result)
print()
result = p.parser.parse("main(x, y, z){x = 1; printf(\"aaa\"); aaa = b;}", lexer=p.lexico.lexico) 
print(result)
print()

p = Parser()

with open('entrada.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

p = Parser()
result = p.parser.parse(file_content, lexer=p.lexico.lexico)
print(result)
print()

tree = parse_tuple_to_tree(result[0])
print_tree(tree)
"""