#static analyser heavily derived from Luzgans approach for tree-sitter https://github.com/Luzgan/time-complexity-mcp/blob/main/src/

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node
from app.modules.ComplexityAnalysis.complexity_math import complexity_from_depth, max_complexity, multiply_complexity
from typing import Iterator 
import re

example_code = """
def main(n):
    x = 1 
    
    
    if(n >= 1):
        return main(n -1)
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
    
    functions = [{
        "name": "count_total_numbers",
        "children": [],
        "complexity": "1",
        "body": "return x",
        "node": None  
    }]
    
    while reached_root == False:    
        node = cursor.node
        if node.type == "function_definition":
            name = node.child_by_field_name("name").text.decode("utf8")
            print("Function found: " + name)
            body = node.child_by_field_name("body")
            complexity, children = analyse_function(node, known_functions=functions)
            function = {
                "name": name,
                "children": children,
                "complexity": complexity,
                "body": body,
                "node": node
            }
            functions.append(function)
            parent_function = any(child == name for child in function["children"] for function in functions)
            if parent_function:
                for f in functions:
                    for child in f["children"]:
                        if child == name:
                            #re analyse function with more known functions 
                            f["complexity"] = analyse_function(f["node"], known_functions=functions)
        
        if cursor.goto_first_child():
            continue  
        
        if cursor.goto_next_sibling():
            continue
        
        retracing = True
        while retracing:
            wentToParent = cursor.goto_parent()
            if not wentToParent:
                retracing = False
                reached_root = True
            elif cursor.goto_next_sibling():
                retracing = False  
    return functions

LOOP_TYPES = ["for_statement", "while_statement"]

def analyse_function(node:Node, known_functions):
    looped_complexity = detect_loops(node, known_functions)
    known_call_complexity = detect_known_calls(node, known_functions)
    
    current_complexity = max_complexity(looped_complexity, known_call_complexity)
    
    recursive_complexity = detect_recursion(node, current_complexity)
    
    print(recursive_complexity)
    
    return recursive_complexity
 


def detect_known_calls(node:Node, known_functions):
    if(known_functions):
        known_names = [function["name"] for function in known_functions]
        known_complexities = [function["complexity"] for function in known_functions]
        highest_complexity = "1"
        for child in iter_nodes(node, LOOP_TYPES):
            #Should not detect known functions in sub-loops since the complexity is dependent on the loop -> detect_loops()
            if child is not None and child.type == "call":
                print(child)
                print(child.child_by_field_name("function").text.decode("utf8"))
                if child.child_by_field_name("function").text.decode("utf8") in known_names:
                    index = known_names.index(child.child_by_field_name("function").text.decode("utf8"))
                    if max_complexity(highest_complexity, known_complexities[index]) != highest_complexity:
                        highest_complexity = known_complexities[index]
                    
        return highest_complexity
    return "1"
        
def detect_loops(func_node:Node, known_calls):
    print("Searching for loops in:" + func_node.child_by_field_name("name").text.decode("utf8"))
    complexity = "1"
    
    loops = []
    
    def walk(node: Node, current_loop_depth):
        if node.type == "function_definition" and node is not func_node:
            return  # don't descend into nested function defs
        if node.type in LOOP_TYPES:
            print(node)
            is_constant = is_constant_loop(node)
            is_logarithmic = (not is_constant) and is_logarithmic_loop(node)
            known_call_complexity = detect_known_calls(node, known_calls)

            if is_constant:
                depth = 0
                complexity = "1"
                complexity = multiply_complexity(complexity, known_call_complexity)
            elif is_logarithmic:
                depth = 0
                complexity = multiply_complexity(
                    complexity_from_depth(current_loop_depth), "log n"
                )
                complexity = multiply_complexity(complexity, known_call_complexity)
            else:
                depth = current_loop_depth + 1
                complexity = complexity_from_depth(depth)
                complexity = multiply_complexity(complexity, known_call_complexity)
                
            loops.append({
                "type": node.type,
                "line": node.start_point[0] + 1,
                "nesting_depth": depth,
                "complexity": complexity,
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
        #Check for `for x in [1, 2, 3]` (literal list)
        if right is not None and right.type == "list": return True
        if right is not None and right.type == "tuple": return True
    return False

                #           some string (+optional space) with either integer division by 2
                #                                                     float division by 2
                #                                                     halving via bit shift >>= 1
                #                                                     doubling
                #                                                     doubling via bit shift 
                #                                                                               \b needs to stop right after so no 20 or 2.5
_LOG_PATTERN = re.compile(r"^[a-zA-Z_]\w*\s*(?://=\s*2|/=\s*2|>>=\s*1|\*=\s*2|<<=\s*1)\b")
    
def is_logarithmic_loop(node: Node):
    if node.type != "while_statement":
        return False
    for child in iter_nodes(node):
        print("Type: " + child.type + " text: " + child.text.decode("utf8"))
        #only accounts for logarithmic loop written like this variable + augmented_assignment operator -> divided or multiplied by 2
        #it also assumes any such assignment within the while loop is indicative of a logarithmic complexity 
        if child.type == "augmented_assignment" and _LOG_PATTERN.match(child.text.decode("utf8")):
            return True
    return False

def iter_nodes(node: Node, stopTypes=[]) -> Iterator[Node]:
    yield node
    for child in node.children:
        if child.type in stopTypes:
            continue
        yield from iter_nodes(child, stopTypes)
    

    
# This flat out ignores mutual recursion -> an attempt is made to still do this kind of with detecting child functions, but it's not really solid
def detect_recursion(node:Node, current_complexity):
    func_name = node.child_by_field_name("name").text.decode("utf8")
    total_calls = 0
    calls_outside_loops = 0
    
    def walk(node:Node, in_Loop=False):
        nonlocal func_name
        nonlocal total_calls
        nonlocal calls_outside_loops
        
        isLoop = node.type in LOOP_TYPES
        currentInLoop = in_Loop or isLoop
        
        if node is not None and node.type == "call":
            if node.child_by_field_name("function").text.decode("utf8") == func_name:
                total_calls += 1
                if not currentInLoop: calls_outside_loops += 1
                #If I were to apply akra bazzi it would be right around here.
                #However, sinc ethe static analyser only outputs, logarithmic, constant, polynomial and exponential the individual variables don't really matter
                
        for child in node.children:
            walk(child)
    walk(node)
    print(total_calls)
    
    if total_calls == 0: return current_complexity
    if calls_outside_loops < total_calls: return multiply_complexity(current_complexity, "n")
    if total_calls == 1: return multiply_complexity(current_complexity, "n")
    if total_calls >= 2:
        if _LOG_PATTERN.match(node.text.decode("utf8")): return multiply_complexity(current_complexity, "n log n")
        return multiply_complexity(current_complexity, "n^2")
            