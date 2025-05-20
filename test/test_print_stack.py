import unittest
import io
import sys
from unittest.mock import patch
from stack import print_stack


class TestPrintStack(unittest.TestCase):

    def setUp(self):
        self.stdout = io.StringIO()
        self.stdout = self.stdout
    
    def tearDown(self):
        sys.stdout = sys.__stdout__
    
    def test_debug_off(self):
        @print_stack
        def sample_func(x):
            return x * 2

        result = sample_func(5)
        self.assertEqual(result, 10)
        self.assertEqual(self.stdout.getvalue(), '')

    @patch.dict('os.environ', {'DEBUG': '1'})
    def test_debug_on(self):
        @print_stack
        def sample_func(x):
            return x * 2
        
        result = sample_func(5)
        output = self.stdout.getvalue()
        self.assertEqual(result, 10)
        self.assertIn(output, 'Entering sample_func')
        self.assertIn(output, 'args (5,)')
        self.assertIn(output, 'Exiting sample_func')

    @unittest.skip
    @patch.dict('os.environ', {'DEBUG': '1'})
    def test_max_depth_exceeded(self):
        @print_stack
        def recursive_func(n):
            if n <= 0: return 0
            return recursive_func(n - 1)

        with self.assertRaises(Exception) as context:
            recursive_func(501)
        self.assertIn(str(context.exception), 'Maximum call stack depth exceeded')
    
    def test_invalid_decorator_input(self):
        with self.assertRaises(TypeError):
            print_stack("not a function")


if __name__ == "__main__":
    unittest.main()