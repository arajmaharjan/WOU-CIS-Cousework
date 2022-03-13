import pytest
from roman import int_to_roman

def test_empty_string():
    """test_empty_string() should test input"""
    assert int_to_roman(0) == ''

def test_vaild_integer():
    """test_vaild_integer() should check an vaild integer input between 0 to 109"""
    with pytest.raises(ValueError):
        int_to_roman(number="Input a integer") 

def test_known_values():
    """test_empty_string() should test known roman values"""
    assert int_to_roman(1) == 'I'
    assert int_to_roman(4) == 'IV'
    assert int_to_roman(5) == 'V'
    assert int_to_roman(9) == 'IX'
    assert int_to_roman(10) == 'X'
    
def testing_single_double_triple_int_to_roman():
    """testing_single_double_triple_int_to_roman() should test single, double and triple roman values conversion"""
    assert int_to_roman (1) == 'I'
    assert int_to_roman (10) == 'X'
    assert int_to_roman (109) == 'CIX'