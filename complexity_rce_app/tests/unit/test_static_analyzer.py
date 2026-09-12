from backend.app.modules.ComplexityAnalysis import static_analysis

function_call_example_code = """
def main(n):
    x = 0
    for i in range(n):
        x += i + foo(n)
    return x
def foo(n):
    return n
"""

finding_main_example_code = """
def main(n):
    return n
"""

def test_finding_main():
    category, degree = static_analysis.calculate_static_complexity(finding_main_example_code)
    assert category == "constant"

def test_function_call():
    category, degree = static_analysis.calculate_static_complexity(function_call_example_code)
    assert category == "polynomial"