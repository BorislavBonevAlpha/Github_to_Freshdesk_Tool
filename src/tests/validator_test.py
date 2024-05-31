import unittest
from common.validators import validate_params_count

class TestValidateParamsCount(unittest.TestCase):
    
    def test_invalid_params_count(self):
        with self.assertRaises(ValueError) as context:
            validate_params_count(['parameter1', 'parameter2'], 3)
        
        self.assertEqual(
            str(context.exception), 
            'Invalid number of arguments. Expected: 3; received: 2.")'
        )