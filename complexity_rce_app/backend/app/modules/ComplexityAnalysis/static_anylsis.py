import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node

example_code = """
def foo(x, y):
    if x > 0:
        return x
    else:
        return y
"""


def calculate_static_complexity(code=example_code, language="python"):
    match language:
        case "python":
            PY_LANGUAGE = Language(tspython.language())
            parser = Parser(PY_LANGUAGE)
            tree = parser.parse(bytes(code, "utf8"))
        case _:
            raise ValueError("Language " + language + " not supported for static analyser.")
    
    functions = extract_functions(tree)
        
def analyse_function(node, current_complexity, loop_depth):
    return "1"
        
def extract_functions(tree: Tree):
    cursor = tree.walk()
    reached_root = False
    
    function_stack = []
    functions = [{}]
    
    while reached_root == False:    
        node = cursor.node
        if node.type == "function_definition":
            name = node.child_by_field_name("name").text.decode("utf8")
            print("Function found: " + name)
            parent_function = function_stack[-1] if function_stack else None
            complexity = analyse_function(node, current_complexity=parent_function.complexity if parent_function else "1", loop_depth=0)
            function = {
                "name": name,
                "parent": parent_function,
                "children": [],
                "parameters": [], #TODO
                "complexity": complexity,
                "body": node.child_by_field_name("body")
            }
            if parent_function:
                for f in functions:
                    if f["name"] == parent_function["name"]:
                        f["children"].append(name)
                        
            function_stack.append(name)   
            functions.append(function)
        
        if cursor.goto_first_child():
            continue  
        
        if cursor.goto_next_sibling():
            continue
        
        retracing = True
        while retracing:
            wentToParent = cursor.goto_parent()
            if cursor.node.type == "function_definition":
                parent = function_stack.pop()
                print("Parent removed: " + parent)
            if not wentToParent:
                retracing = False
                reached_root = True
            elif cursor.goto_next_sibling():
                retracing = False  
    return functions