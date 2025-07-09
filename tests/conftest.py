import sys
import pytest
import time

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from hash_manager import HashWrapper, HashManager
from utils import Utils

sleep_time = 0


@pytest.fixture
def hash_wrapper():
    wrapper = HashWrapper()
    wrapper.HashInit()
    yield wrapper
    time.sleep(sleep_time)
    wrapper.HashTerminate()


@pytest.fixture
def hash_manager(hash_wrapper):
    manager = HashManager(hash_wrapper)
    manager.initialize()
    yield manager
    time.sleep(sleep_time)
    manager.terminate()


@pytest.fixture
def utils(hash_wrapper):
    return Utils(hash_wrapper)
