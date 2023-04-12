from Sintatico import parse_tuple_to_tree, print_tree, TreeNode, Parser

class Semantico():
    def __init__(self, tree):
        self.tree = tree
        self.tabela_simbolo = {}
        
    def resolve_conta(self, node):
        if isinstance(node, TreeNode):            
            expression = (node.type, node.value[0], node.value[1])
        else:
            expression = node
        if isinstance(expression, (int, float)):
            return expression
        elif expression[0] == 'ADD':
            return self.resolve_conta(expression[1]) + self.resolve_conta(expression[2])
        elif expression[0] == 'SUB':
            return self.resolve_conta(expression[1]) - self.resolve_conta(expression[2])
        elif expression[0] == 'MUL':
            return self.resolve_conta(expression[1]) * self.resolve_conta(expression[2])
        elif expression[0] == 'DIV':
            return self.resolve_conta(expression[1]) / self.resolve_conta(expression[2])
        return expression
    
    def verifica_tabela_simbolo(self, node):
        if node.type == "ATRIBUITION":
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
                    self.tabela_simbolo.update({node.value[0]: [valor_att, type(valor_att)]})
        
    def verifica_tipo(self, node):
        if node.type in {"ADD", "SUB", "MUL", "DIV"}:
            if isinstance(node.value, tuple) and len(node.value) == 2:
                if not (isinstance(node.value[0], (int,float)) or isinstance(node.value[1], (int,float))): 
                    # Verifica se está tentantando fazer operação com tipos diferentes fora numeros 
                    if type(node.value[0]) != type(node.value[1]):
                        raise ValueError("Erro semantico em ", node.value)
                    # Verifica se esta fazendo operação com string
                    elif type(node.value[0]) == str or type(node.value[1]) ==  str:
                        raise ValueError("Erro semantico em ", node.value)
                    # Verifica se esta fazendo operação com boolean
                    elif type(node.value[0]) == bool or type(node.value[1]) ==  bool:
                        raise ValueError("Erro semantico em ", node.value)
                        
                        
    def verifica_existencia(self, node):
        if node.type in {"IF"}:
            if isinstance(node.value, str) and node.value not in ("true", "false"):
                if not node.value in self.tabela_simbolo:
                    raise ValueError(f"Variavel não declarada {node.value}")  
            elif isinstance(node.value, tuple):
                if isinstance(node.value[2], str):
                    # Verifica se existe na tabela simbolo
                    if not node.value[2] in self.tabela_simbolo:
                        raise ValueError(f"Variavel não declarada {node.value[2]}")
                if isinstance(node.value[3], str):
                    # Verifica se existe na tabela simbolo
                    if not node.value[3] in self.tabela_simbolo:
                        raise ValueError(f"Variavel não declarada {node.value[3]}")            
                
        if node.type in {"WHILE"}:
            if isinstance(node.value, str) and node.value not in ("true", "false"):
                if not node.value in self.tabela_simbolo:
                    raise ValueError(f"Variavel não declarada {node.value}")  
            elif isinstance(node.value, tuple):
                if isinstance(node.value[2], str):
                    # Verifica se existe na tabela simbolo
                    if not node.value[2] in self.tabela_simbolo:
                        raise ValueError(f"Variavel não declarada {node.value[2]}")
                if isinstance(node.value[3], str):
                    # Verifica se existe na tabela simbolo
                    if not node.value[3] in self.tabela_simbolo:
                        raise ValueError(f"Variavel não declarada {node.value[3]}") 


        # Fazer pro print
        # Else talvez, mas é mais complicado
    def walk_tree(self, node, level=0):
        print(self.tabela_simbolo)
        #print(' ' * level * 4 + f'{node.type}: {node.value}')
        for child in node.children:
            self.verifica_tipo(child)
            self.verifica_tabela_simbolo(child)
            self.verifica_existencia(child)
            self.walk_tree(child, level+1)
    
p = Parser()
with open('entrada_emoji.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

p = Parser()
result = p.parser.parse(file_content, lexer=p.lexico.lexico)
tree = parse_tuple_to_tree(result[0])
print_tree(tree)

s = Semantico(tree);
s.walk_tree(tree)

