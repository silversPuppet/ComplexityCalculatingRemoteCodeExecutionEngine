import unittest
from backend.app.modules.ComplexityAnalysis.static_analysis import calculate_static_complexity

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


class TestCalculateStaticComplexity(unittest.TestCase):
    def test_finding_main(self):
        category, degree = calculate_static_complexity(finding_main_example_code)
        self.assertEqual(category, "constant")

    def test_function_call(self):
        category, degree = calculate_static_complexity(function_call_example_code)
        self.assertEqual(category, "polynomial")