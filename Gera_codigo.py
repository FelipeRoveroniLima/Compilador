from Semantic import Semantico
from Sintatico import parse_tuple_to_tree, print_tree, TreeNode, Parser

class Code_generator():

    def __init__(self, tree):
        self.tree = tree
        self.code = ""
        
    def tuple_to_string(self, t):                                                                                                                                                                                                                                                                                                                        
        print(t)
        if isinstance(t, (int,float)):
            return str(t)
        elif isinstance(t, str):
            return t
        else:
            op, left, right = t
            left_str = self.tuple_to_string(left)
            right_str = self.tuple_to_string(right)
            op_str = " " + op + " "
            if op == "ADD":
                op_str = " + "
            if op == "SUB":
                op_str = " - "
            elif op == "MUL":
                op_str = " * "
            elif op == "DIV":
                op_str = " / "
            return left_str + op_str + right_str
    def generate(self, node, level=0):
        
        if node.type == 'FUNCTION':
            if len(node.value) > 1:   
                variaveis = node.value[1]  
                variables_str = ", ".join(variaveis)  
                self.code += f"def {node.value[0]} ({variables_str}):\n"
            else:
                self.code += f"def {node.value[0]} ():\n"
                
        if node.type == "ATRIBUITION":
            if node.children == []:   
                self.code += ' ' * level * 4 + f"{node.value[0]} = {node.value[1]}\n"
            else:
                operacoes = node.children[0].value
                operacoes = self.tuple_to_string(operacoes)
                self.code += ' ' * level * 4 + f"{node.value[0]} = {operacoes}\n"

        if node.type == "PRINTF":
            if isinstance(node.value, tuple):
                type, value = node.value
                self.code += ' ' * level * 4 + f"print(\"{value}\")\n"
            else:
                self.code += ' ' * level * 4 + f"print({node.value})\n"
            
        if node.type == 'IF' :
            if isinstance(node.value, (int, float)):
                self.code += ' ' * level * 4 + f"if ({node.value}):\n"             
            elif len(node.value) == 1:
                self.code += ' ' * level * 4 + f"if ({node.value}):\n"            
            elif len(node.value) == 4: 
                if isinstance(node.value[3], tuple):
                    operacoes3 = self.tuple_to_string(node.value[3])
                else:
                    operacoes3 =  node.value[3]

                if isinstance(node.value[2], tuple):
                    operacoes2 = self.tuple_to_string(node.value[2])    
                else:
                    operacoes2 = node.value[2]                    

                self.code += ' ' * level * 4 + f"if ({operacoes2} {node.value[1]} {operacoes3}):\n"

        if node.type == 'WHILE':
            if isinstance(node.value, (int, float)) or node.value == "True" or node.value == "False":
                self.code += ' ' * level * 4 + f"while ({node.value}):\n"             
            elif len(node.value) == 1:
                self.code += ' ' * level * 4 + f"while ({node.value}):\n"            
            elif len(node.value) == 4: 
                if isinstance(node.value[3], tuple):
                    operacoes3 = self.tuple_to_string(node.value[3])
                else:
                    operacoes3 =  node.value[3]

                if isinstance(node.value[2], tuple):
                    operacoes2 = self.tuple_to_string(node.value[2])    
                else:
                    operacoes2 = node.value[2]                    

                self.code += ' ' * level * 4 + f"while ({operacoes2} {node.value[1]} {operacoes3}):\n"
        
        if node.type == 'IF_ELSE':
            for i in node.value[1]:
                node_aux = TreeNode(i[0], i[1])
                aux = self.generate(node_aux, level)
                
            if isinstance(node.value[0], (int, float)) == 1:
                self.code += ' ' * level * 4 + f"if ({node.value}):\n"             
            elif len(node.value[0]) == 1:
                self.code += ' ' * level * 4 + f"if ({node.value}):\n"            
            elif len(node.value[0]) == 4: 
                if isinstance(node.value[0][3], tuple):
                    operacoes3 = self.tuple_to_string(node.value[0][3])
                else:
                    operacoes3 =  node.value[0][3]

                if isinstance(node.value[0][2], tuple):
                    operacoes2 = self.tuple_to_string(node.value[0][2])    
                else:
                    operacoes2 = node.value[0][2]                    

                self.code += ' ' * level * 4 + f"if ({operacoes2} {node.value[0][1]} {operacoes3}):\n"
                # Recursão 

                for i in node.value[1]:
                    node_aux = TreeNode(i[0], i[1])
                    self.generate(node_aux, level)

        for child in node.children:
            self.generate(child, level+1)
        
    def generate_call(self, tree):
        #if tree.value[1] != 
        variaveis = tree.value[1]  
        for i in range(len(variaveis)):
            variaveis[i] += '= 0'
        variables_str = ", ".join(variaveis) 
        
        self.code += f"\n{tree.value[0]}({variables_str})"


p = Parser()
with open('entrada_emoji.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

p = Parser()
result = p.parser.parse(file_content, lexer=p.lexico.lexico)
tree = parse_tuple_to_tree(result[0])
print_tree(tree)

s = Semantico(tree);
s.walk_tree(tree)
c = Code_generator(tree)
c.generate(tree)
c.generate_call(tree)
print(c.code)

with open('out.py', 'w', encoding='utf-8') as file:
    file.write(c.code)
