# import inspect
import ast, astunparse
from typing import Any
import os
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




def __getDefClosure(root, nonLocalContext, aliasNotion):
    resultSet = list()
    localContext = dict(nonLocalContext)
    localAliasNotion = dict(aliasNotion)
    for node in ast.iter_child_nodes(root):
        
        if isinstance(node, ast.Import):
            pass#add to localContext, add alias notation
        elif isinstance(node, ast.ClassDef):
            classResult = __getDefClosure(node, localContext, localAliasNotion)
        elif isinstance(node, ast.Assign):
            pass#add to localContext, no alias
    return resultSet


def getDefs(filename):
    with open(filename,'r') as f:            
        parsed = ast.parse(f.read())
        parsed = deAliasTransformer().visit(parsed)
        parsed = __filterAST(parsed)
        print(astunparse.unparse(parsed))