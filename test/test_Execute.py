from tool.Execute import execute

from logging import getLogger
from logging.config import fileConfig
import os


fileConfig(os.path.join(os.path.dirname(__file__), 'logging.ini'))
logger = getLogger(__name__)


def test_execute1():
    exe = execute('./data/test2.txt')
    (b, c) = exe.execute(0, 1)
    assert b == ['0x12']

def test_execute2():
    exe = execute('./data/test2.txt')
    (b, c) = exe.execute(0, 2)
    assert b == ['0x12', '0x34']

def test_get1():
    exe = execute('./data/test2.txt')
    (b, c) = exe.get(1)
    assert b == ['0x12']
    (b, c) = exe.get(1)
    assert b == ['0x34']