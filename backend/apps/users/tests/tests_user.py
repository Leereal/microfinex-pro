import pytest

def test_new_user(new_user):
    print(new_user.first_name)
    assert new_user.first_name == 'test'
