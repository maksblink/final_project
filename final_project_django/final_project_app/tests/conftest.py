import pytest

from utils import create_fake_user, create_fake_group


@pytest.fixture
def set_up():
    create_fake_group()
    for _ in range(10):
        create_fake_user()
