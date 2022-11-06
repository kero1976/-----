from tool.Analyze import analyze

from logging import getLogger
from logging.config import fileConfig
import os


fileConfig(os.path.join(os.path.dirname(__file__), 'logging.ini'))
logger = getLogger(__name__)


def test_head1():
    exe = analyze('./data/test2.txt')
    result = exe.head()
    assert result == ["分割区分:['0x12']", "レコード区分:['0x34']", "運用モード:['0x56']"]