#derived from https://github.com/Luzgan/time-complexity-mcp/blob/main/src/analyzer/complexity.ts

#static analysis only handles these selective complexities, because preliminary factors aren't that important for overall trends and the comparison only happens between larger trends anyway 
COMPLEXITY_ORDER = ["1", "log n", "n log n", "n", "n^2", "n^3", "2^n"]

#instead of meticulously adding complexity we will just take the worst-case one 
def max_complexity(a, b):
    if a == "unknown" or b == "unknown": return "unknown"
    
    if COMPLEXITY_ORDER.index(a) >= COMPLEXITY_ORDER.index(b):
        return a
    else:
        return b

def multiply_complexity(inner, outer):
    #handles nested operations 
    if outer == "unknown" or inner == "unknown": return "unknown"
    if outer == "1": return inner
    if inner == "1": return outer
    
    multiplication_table = {
        "n*n": "n^2",
        "n*log n": "n log n",
        "n*n log n": "n^2",
        "n*n^2": "n^3",
        "n^2*n": "n^3",
        "log n*n": "n log n",
        "log n*log n": "log n",
    }
    
    key = inner + "*" + outer
    reverseKey = outer + "*" + inner
    
def complexity_from_depth(depth):
    if depth <= 0: return "1"
    if depth == 1: return "n"
    if depth == 2: return "n^2"
    if depth >= 2: return "n^3"