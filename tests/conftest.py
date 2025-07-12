import sys
import pytest
import time

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from hash_manager import HashWrapper, HashManager
from utils import Utils

sleep_time = 0.5


# TODO: Remove the read_remained_lines() function after "Terminate() doesn't clean memory" bug fixed
def read_remained_lines(hash_manager: HashManager):
    while True:
        try:
            hash_manager.read_next_log_line_and_free()
        except:
            break


@pytest.fixture
def hash_wrapper():
    wrapper = HashWrapper()
    wrapper.HashInit()
    try:
        yield wrapper
    finally:
        read_remained_lines(HashManager(wrapper))
        wrapper.HashTerminate()


@pytest.fixture
def hash_wrapper_no_types():
    wrapper = HashWrapper(setup_types=False)
    wrapper.HashInit()
    try:
        yield wrapper
    finally:
        # TODO: Remove the line below after "Terminate() doesn't clean memory" bug fixed
        read_remained_lines(HashManager(wrapper))
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
        # TODO: Remove the line below after "Terminate() doesn't clean memory" bug fixed
        read_remained_lines(manager)
        # TODO: Remove line below when "HashStop / HashTerminate - Freeze if the operation is not yet complete" bug fixed
        time.sleep(sleep_time)
        manager.terminate()


@pytest.fixture
def utils(hash_wrapper):
    return Utils(hash_wrapper)
