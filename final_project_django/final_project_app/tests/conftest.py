import pytest
from utils import create_fake_user


@pytest.fixture
def set_up():
    for _ in range(10):
        create_fake_user()
