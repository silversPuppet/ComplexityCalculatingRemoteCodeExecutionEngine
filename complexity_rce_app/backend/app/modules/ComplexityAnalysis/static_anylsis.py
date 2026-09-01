#static analyser heavily derived from Luzgans approach for tree-sitter https://github.com/Luzgan/time-complexity-mcp/blob/main/src/

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node
from app.modules.ComplexityAnalysis.complexity_math import complexity_from_depth, max_complexity, multiply_complexity

example_code = """
def foo(x, y):
    for i in range(3):
        x += y 
    return x 
"""


def calculate_static_complexity(code=example_code, language="python"):
    match language:
        case "python":
            PY_LANGUAGE = Language(tspython.language())
            parser = Parser(PY_LANGUAGE)
            tree = parser.parse(bytes(code, "utf8"))
        case _:
            raise ValueError("Language " + language + " not supported for static analyser.")
    
    topComplexity = "0"
    functions = extract_functions(tree)
    for f in functions:
        if f["name"] == "main":
            topComplexity = f["complexity"]
    
            
#Walks dfs through the tree and analyses complexity of functions it finds 
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
            body = node.child_by_field_name("body")
            complexity = analyse_function(node, known_functions=functions)
            function = {
                "name": name,
                "parent": parent_function,
                "children": [],
                "complexity": complexity,
                "body": body,
                "node": node
            }
            functions.append(function)
            if parent_function:
                for f in functions:
                    if f["name"] == parent_function["name"]:
                        f["children"].append(name)
                        f["complexity"] = analyse_function(f["node"])
            function_stack.append(name) #TODO: this is wrong (assumes function definition is child of function call which isn't the case for syntax trees) -> need to identify which function calls which 
        
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

def analyse_function(node:Node, known_functions):
    #used for things like library calls 
    known_calls = detect_known_calls(node)
    
    looped_complexity = detect_loops(node, known_functions, known_calls)
    
    recursive_complexity = detect_recursion(node)
    
    return looped_complexity + recursive_complexity
 
    

def detect_known_calls(node:Node):
    return []    
    
def detect_loops(func_node:Node, known_functions, known_calls):
    print("Searching for loops in:" + func_node.child_by_field_name("name").text.decode("utf8"))
    loop_types = ["for_statement", "while_statement"]
    complexity = "1"
    
    loops = []
    
    def walk(node: Node, current_loop_depth):
        if node.type == "function_definition" and node is not func_node:
            return  # don't descend into nested function defs
        if node.type in loop_types:
            print(node.type)
            is_constant = is_constant_loop(node)
            is_logarithmic = (not is_constant) and is_logarithmic_loop(node)

            if is_constant:
                depth = 0
                complexity = "1"
            elif is_logarithmic:
                depth = 0
                complexity = multiply_complexity(
                    complexity_from_depth(current_loop_depth), "log n"
                )
            else:
                depth = current_loop_depth + 1
                complexity = complexity_from_depth(depth)
                
            loops.append({
                "type": node.type,
                "line": node.start_point[0] + 1,   # start_point is (row, col), 0-indexed
                "nesting_depth": depth,
                "estimated_complexity": complexity,
            })

            child_depth = current_loop_depth if (is_constant or is_logarithmic) else current_loop_depth + 1
            for child in node.children:
                walk(child, child_depth)
            return

        for child in node.children:
            walk(child, current_loop_depth)
            
    walk(func_node, 0)
    print(loops)
    for l in loops:
        if max_complexity(complexity, l["complexity"]) != complexity:
            complexity = l["complexity"]
    return complexity

def is_constant_loop(node: Node):
    print(node)
    if node.type == "for_statement":
        right = node.child_by_field_name("right")
        if right is not None and right.type == "call":
            print(right)
            funcNode = right.child_by_field_name("function")
            if funcNode is not None and funcNode.type == "identifier" and funcNode.text.decode("utf8") == "range":
                args = right.child_by_field_name("arguments")
                if args:
                    #checks if all arguments are integer literals
                    allLiteral = True
                    for i in range(args.child_count):
                        arg = args.child(i)
                        if not arg or arg.type == "(" or arg.type == ")" or arg.type == ",": continue 
                        hasArg = True
                        if arg.type != "integer":
                            allLiteral = False
                    if hasArg and allLiteral: return True
    
def is_logarithmic_loop(node):
    pass

def detect_recursion(node:Node):
    return "1"