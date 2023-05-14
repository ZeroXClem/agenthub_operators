import sys
from pathlib import Path
# Add the parent directory of this package to PATH so that to 
# make it possible to import other package from here, e.g. util
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unittest.mock import Mock, patch
import unittest

from .mock_ai_context import MockAiContext

from .tester import test_operator

class ListProcessorTest(unittest.TestCase):
    def test_list_processor(self):
        guess_animal_step = {
            "operator":"List Processor",
            "parameters" : {
                "prompt":"Based on a description of an animal below guess which one it is, output only one word, which is name of an animal. Use only lowercase characters and don't add dot at the end."
            }
        }
        
        all_tests = [
            {
                'step': guess_animal_step,
                'inputs': {
                    'list': [
                        {'name': 'tbd', 'content': 'has 4 legs and barks'},
                        {'name': 'tbd', 'content': 'has 2 legs and is destroying the earth ecosystem'}
                    ]
                },
                'expected_outputs': {
                    'result_list': [
                        {'name': 'tbd', 'content': 'dog'},
                        {'name': 'tbd', 'content': 'human'}
                    ]
                }
            }
        ]
        
        with patch('ai_context.AiContext', new=MockAiContext):
            from operators import ListProcessor
            test_operator(all_tests, ListProcessor, self)


