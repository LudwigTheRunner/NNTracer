# import inspect
import ast, astunparse
from typing import Any
import copy
class deAliasTransformer(ast.NodeTransformer):
    aliasMap = dict()
    def generic_visit(self, node: ast.AST) -> ast.AST:
        ast.NodeVisitor.generic_visit(self, node)
        return node

    def visit_alias(self, node: ast.alias) -> Any:
        if node.asname:
            if node.asname in self.aliasMap.keys():
                raise("Conflict alias for ", node.asname)
            self.aliasMap[node.asname] = node.name
        ast.NodeVisitor.generic_visit(self, node)
        delattr(node, 'asname')
        return node

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id in self.aliasMap.keys():
            node.id = self.aliasMap[node.id]
        ast.NodeVisitor.generic_visit(self, node)
        return node
    
    def visit_Module(self, node: ast.Module) -> Any:
        filtered_node = copy.copy(node)
        filtered_node.body = []
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Import) or isinstance(child, ast.ImportFrom) \
                or isinstance(child, ast.ClassDef) or isinstance(child, ast.FunctionDef) \
                    or isinstance(child, ast.AsyncFunctionDef):
                        filtered_node.body.append(child)
        ast.NodeVisitor.generic_visit(self, node)
        return node


def __filterAST(mod: ast.Module):
    filtered_node = copy.copy(mod)
    filtered_node.body = []
    for child in ast.iter_child_nodes(mod):
        if isinstance(child, ast.Import) or isinstance(child, ast.ImportFrom) \
            or isinstance(child, ast.ClassDef) or isinstance(child, ast.FunctionDef) \
                or isinstance(child, ast.AsyncFunctionDef):
                    filtered_node.body.append(child)
    return filtered_node


def getDefs(filename):
    with open(filename,'r') as f:            
        parsed = ast.parse(f.read())
        parsed = deAliasTransformer().visit(parsed)
        parsed = __filterAST(parsed)
        with open('dummy.py', 'w') as w:
            w.write(astunparse.unparse(parsed))


import tokenize

with tokenize.open('hello.py') as f:
    tokens = tokenize.generate_tokens(f.readline)
    for token in tokens:
        print(token)