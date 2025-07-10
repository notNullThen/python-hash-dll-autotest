import sys
import pytest
import time

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from hash_manager import HashWrapper, HashManager
from utils import Utils


@pytest.fixture
def hash_wrapper():
    wrapper = HashWrapper()
    wrapper.HashInit()
    try:
        yield wrapper
    finally:
        wrapper.HashTerminate()


@pytest.fixture
def hash_wrapper_no_types():
    wrapper = HashWrapper(setup_types=False)
    wrapper.HashInit()
    try:
        yield wrapper
    finally:
        wrapper.HashTerminate()


@pytest.fixture
def hash_manager(hash_wrapper):
    manager = HashManager(hash_wrapper)
    manager.initialize()
    try:
        yield manager
    finally:
        manager.terminate()


@pytest.fixture
def utils(hash_wrapper):
    return Utils(hash_wrapper)
