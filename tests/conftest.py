import sys

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

import pytest
from hash_manager import HashWrapper, HashManager
from utils import Utils


@pytest.fixture
def hash_wrapper():
    wrapper = HashWrapper()
    wrapper.HashInit()
    yield wrapper
    wrapper.HashTerminate()


@pytest.fixture
def hash_manager(hash_wrapper):
    manager = HashManager(hash_wrapper)
    manager.initialize()
    yield manager
    manager.terminate()


@pytest.fixture
def utils(hash_wrapper):
    return Utils(hash_wrapper)
