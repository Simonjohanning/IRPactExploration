import helper
# test_with_pytest.py

def convert_grid_test():
    assert helper.convertGridInMode(0.3, 0.7, 'PVact') == {'AT': 0.3, 'IT': 0.7}

def convert_grid_testFail():
    assert helper.convertGridInMode(0.3, 0.7, 'PVacta') == {'AT': 0.3, 'IT': 0.7}

def test_always_fails():
    assert False
