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
        result.append(self.format('予約領域', 12))
        result.append(self.format('情報区分', 4))
        result.append(self.format('[第1]No.1', 3))
        result.append(self.format('[第1]No.2', 3))
        result.append(self.format('フォーマットID', 2))
        result.append(self.format('予約領域', 10))
        result.append(self.format('作成日時時刻', 12))
        result.append(self.format('予約領域', 10))
        result.append(self.format('シンタックスID', 6))
        result.append(self.format('拡張モード', 1))
        result.append(self.format('文字コード8', 1))
        result.append(self.format('文字コード16', 1))
        result.append(self.format('非透過', 1))
        result.append(self.format('[第2]No.1', 5))
        result.append(self.format('[第2]No.2', 5))
        result.append(self.format('予約領域', 89))
        result.append(self.format('改行？', 3))
        logger.debug('■終了ポジション:{}'.format(self.exe.first))
        return result

    def message_group(self):
        result = []
        logger.info('メッセージヘッダ開始位置'.format(self.exe.first))
        result.append(self.format('分割区分', 1))
        result.append(self.format('レコード区分', 1))
        result.append(self.format('シーケンス番号', 5))
        
        datasize = self.exe.getint2()
        result.append(' サイズ:{}'.format(datasize))
        
        return result

    def get_tfd_manager(self):
        data = self.get_tfd1()
        for i in data:
            print(i)
        
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

    def get_tfd1(self):
        result = []
        no = self.exe.getint1()
        result.append('項目番号:{}'.format(no))
        len = self.exe.getint1()
        result.append('桁数:{}'.format(len))
        data = self.exe.get(len)
        result.append('データ:{}({})'.format(' '.join(data[0]), ''.join(data[1])))
        return result