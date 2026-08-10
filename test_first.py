# A tiny function to test
def add(a, b):
    return a + b


# A test for that function.
# pytest automatically runs any function whose name starts with "test_".
def test_add_positive_numbers():
    assert add(2, 3) == 6


def test_add_negative_numbers():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(0, 5) == 5

 
