from Semantic import Semantico
from Sintatico import parse_tuple_to_tree, print_tree, TreeNode, Parser

class Code_generator():

    def __init__(self, tree):
        self.tree = tree
        self.code = ""
        self.tabela_simbolo = {}
        
    def tuple_to_string(self, t):
        if isinstance(t, int):
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
        if node.type in ["FUNCTION", "WHILE", "IF", "ELSE"]:
            if len(node.value) > 1:   
                variaveis = node.value[1]  
                variables_str = ", ".join(variaveis)  
                self.code += f"def {node.value[0]} ({variables_str}):\n"
            else:
                self.code += f"def {node.value[0]} ():\n"
                
        if node.type == "ATRIBUITION":
            print("aa")
            if node.children == []:   
                self.code += ' ' * level * 4 + f"{node.value[0]} = {node.value[1]}\n"
            else:
                operacoes = node.children[0].value
                operacoes = self.tuple_to_string(operacoes)
                self.code += ' ' * level * 4 + f"{node.value[0]} = {operacoes}\n"

        if node.type == "PRINTF":
            self.code += ' ' * level * 4 + f"print(\"{node.value}\")\n"

        # if
        # while
        # else

        for child in node.children:
            self.generate(child, level+1)




p = Parser()
with open('entrada.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

p = Parser()
result = p.parser.parse(file_content, lexer=p.lexico.lexico)
tree = parse_tuple_to_tree(result[0])
print_tree(tree)

s = Semantico(tree);
s.walk_tree(tree)
c = Code_generator(tree)
c.generate(tree)
print(c.code)

"""
FUNCTION: ('main', ['x', 'y'])
    ATRIBUITION: ('x', 0)
    ATRIBUITION: x
        SUB: (('ADD', 3, 'x'), 1)
    IF: x
        PRINTF: aaaaaa
    WHILE: 1
        IF: ('COMPARE', '<', 'x', 1)
            PRINTF: bbbbb
"""