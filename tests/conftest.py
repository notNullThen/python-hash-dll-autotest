import sys
import pytest
import time

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from hash_manager import HashWrapper, HashManager
from utils import Utils

sleep_time = 0.5


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
        # TODO: Remove line below when "HashStop / HashTerminate - Freeze if the operation is not yet complete" bug fixed
        time.sleep(sleep_time)
        wrapper.HashTerminate()


@pytest.fixture
def hash_manager(hash_wrapper):
    manager = HashManager(hash_wrapper)
    manager.initialize()
    try:
        yield manager
    finally:
        # TODO: Remove line below when "HashStop / HashTerminate - Freeze if the operation is not yet complete" bug fixed
        time.sleep(sleep_time)
        manager.terminate()


@pytest.fixture
def utils(hash_wrapper):
    return Utils(hash_wrapper)
