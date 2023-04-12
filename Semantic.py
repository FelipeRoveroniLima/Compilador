# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 20:07:49 2023

@author: sergi
"""

from Sintatico import parse_tuple_to_tree, print_tree, TreeNode, Parser



class Semantico():
    def __init__(self, tree):
        self.tree = tree
        self.tabela_simbolo = {}
        
    def resolve_conta(self, node):
        if isinstance(node,TreeNode):            
            expression = (node.type, node.value[0], node.value[1])
        else:
            expression = node
        if isinstance(expression, str):
            return int(expression)
        elif expression[0] == 'ADD':
            return self.resolve_conta(expression[1]) + self.resolve_conta(expression[2])
        elif expression[0] == 'SUB':
            return self.resolve_conta(expression[1]) - self.resolve_conta(expression[2])
        elif expression[0] == 'MUL':
            return self.resolve_conta(expression[1]) * self.resolve_conta(expression[2])
        elif expression[0] == 'DIV':
            return self.resolve_conta(expression[1]) / self.resolve_conta(expression[2])
    
    def verifica_tabela_simbolo(self, node):
        if node.type == "ATRIBUITION":
            print(f'{node.type}: {node.value}')
            if node.children == []:
                if node.value in self.tabela_simbolo:
                    print("ta aqui ja", node.value)
                    self.tabela_simbolo[node.value[0]] = [node.value[1], type(node.value[1])]
                else:
                    self.tabela_simbolo.update({node.value[0]: [node.value[1], type(node.value[1])]})
            else:
                if node.value in self.tabela_simbolo:
                    self.tabela_simbolo[node.value[0]] = node.children[0]
                else:
                    valor_att = self.resolve_conta(node.children[0])
                    self.tabela_simbolo.update({node.value[0]: valor_att})
        print(self.tabela_simbolo)
        
    def verifica_tipo(self, node):
        if node.type in {"ADD", "SUB", "MUL", "DIV"}:
            if isinstance(node.value, tuple) and len(node.value) == 2:
                # Verifica se está tentantando fazer operação de string com numero
                if type(node.value[0]) != type(node.value[1]):
                    print("Erro semantico em ", node.value)
                # Verifica se esta fazendo operação com string
                elif type(node.value[0]) == str or type(node.value[1]) ==  str:
                    print("Erro semantico em ", node.value)

    def verifica_existencia(self, node):
        if node.type in {"COMPARE"}:
            print("a")
        
    def walk_tree(self, node, level=0):
        #print(' ' * level * 4 + f'{node.type}: {node.value}')
        for child in node.children:
            self.verifica_tipo(child)
            self.verifica_tabela_simbolo(child)
            self.walk_tree(child, level+1)
    


p = Parser()
with open('entrada.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

p = Parser()
result = p.parser.parse(file_content, lexer=p.lexico.lexico)
tree = parse_tuple_to_tree(result[0])
print_tree(tree)

s = Semantico(tree);
s.walk_tree(tree)