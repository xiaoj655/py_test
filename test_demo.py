import pytest

@pytest.fixture
def x():
    return 2

@pytest.fixture
def y():
    return 2

def test_add(x,y):
    assert 2+2==4
    return 1