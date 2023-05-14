from unittest.mock import Mock, patch

from .mock_ai_context import MockAiContext


#@patch('ai_context.AiContext', new=MockAiContext)
def test_operator(tests, op_type, test_class_instance):

    for t in tests:
        step = t['step']
        ai_context = MockAiContext()
        for input_name, input_val in t['inputs'].items():
            ai_context.set_input(input_name, input_val)
            
        op = op_type()
        op.run_step(t['step'], ai_context)
        
        for output_name, expected_output_val in t['expected_outputs'].items():
            actual_output = ai_context.get_output(output_name)
            
            test_class_instance.assertEqual(expected_output_val, actual_output)
        
        
