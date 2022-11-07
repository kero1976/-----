from logging import getLogger
import unicodedata

logger = getLogger(__name__)


class cii_trailer():

    def __init__(self, exe):
        self.exe = exe

    def print(self):
        datas = self.get()
        for i in datas:
            print(i)
            
    def get(self):
        result = []
        result.append(self.format('分割区分', 1))
        result.append(self.format('レコード区分', 1))
        result.append(self.format('最終シーケンス番号', 5))
        result.append(self.format('項目No1合計', 15))
        result.append(self.format('項目No2合計', 15))
        result.append(self.format('予約領域', 214))
        logger.debug('■終了ポジション:{}'.format(self.exe.first))
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
        result = '{:{width}s}:{}({})'.format(name, ' '.join(data[0]), ''.join(data[1]), width=col)
        return result