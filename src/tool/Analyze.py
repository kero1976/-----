from logging import getLogger
from Execute import execute
logger = getLogger(__name__)


class analyze():
    def __init__(self, file):
        self.file = file
        self.exe = execute(file)

    def head(self):
        result = []
        result.append('分割区分:{}'.format(self.exe.get(1)[0]))
        result.append('レコード区分:{}'.format(self.exe.get(1)[0]))
        result.append('運用モード:{}'.format(self.exe.get(1)[0]))

        return result