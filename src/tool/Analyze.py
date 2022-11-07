from logging import getLogger
from tool.Execute import execute
import unicodedata

logger = getLogger(__name__)


class analyze():
    def __init__(self, file):
        self.file = file
        self.exe = execute(file)

    def head(self):
        result = []
        result.append(self.format('分割区分', 1))
        result.append(self.format('レコード区分', 1))
        result.append(self.format('運用モード', 1))
        result.append(self.format('発信VANセンターコード', 12))
        result.append(self.format('発信センターコード', 12))
        result.append(self.format('発信者コード', 12))
        result.append(self.format('受信VANセンターコード', 12))
        result.append(self.format('受信センターコード', 12))
        result.append(self.format('受信者コード', 12))
        result.append(self.format('[BPID]機関コード', 4))
        result.append(self.format('[BPID]サブ機関コード', 2))
        result.append(self.format('[BPID]バージョン', 2))

        return result

    def format(self, name, size):
        """
        全角が含む場合でも桁そろえ
        https://mulberrytassel.com/python-practice-zenhan/
        """
        data = self.exe.get(size)
        count = 0
        for c in name:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 1
        col = 20 - count
        result = '{:{width}s}:{}({})'.format(name, data[0], data[1], width=col)
        return result