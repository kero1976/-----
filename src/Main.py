from logging import getLogger
from logging.config import fileConfig
import os
import tool.Execute as Execute

fileConfig(os.path.join(os.path.dirname(__file__), 'logging.ini'))
logger = getLogger(__name__)



if __name__ == '__main__':
    exe = Execute.execute('./data/test1.txt')
    exe.execute()