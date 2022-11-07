from logging import getLogger
from tool.Execute import execute
import unicodedata

logger = getLogger(__name__)


class analyze():
    def __init__(self, file):
        self.file = file
        self.exe = execute(file)



    def control(self):

        (data, size) = self.message_group()
        for i in data:
            print(i)
        tfd = self.get_tfd_manager()
        for i in tfd:
            print(i)
        buff = (self.exe.first % 251)
        buff_size = 251 - buff
        logger.info('空白サイズ:{}'.format(buff_size))
        self.exe.get(buff_size)

    def trailer(self):
        result = []
        result.append(self.format('分割区分', 1))
        result.append(self.format('レコード区分', 1))
        result.append(self.format('最終シーケンス番号', 5))
        result.append(self.format('項目No1合計', 15))
        result.append(self.format('項目No2合計', 15))
        result.append(self.format('予約領域', 214))

        return result


    def message_group(self):
        result = []
        logger.info('メッセージヘッダ開始位置:{}'.format(self.exe.first))
        result.append(self.format('分割区分', 1))
        result.append(self.format('レコード区分', 1))
        result.append(self.format('シーケンス番号', 5))
        
        datasize = self.exe.getint2()
        result.append(' サイズ:{}'.format(datasize))
        
        return (result, datasize)

    def get_tfd_manager(self):
        result = []
        while True:
            (data, no) = self.get_tfd1()
            if no >= 240:
                next = self.exe.getint1()
                if next == 250:
                    # マルチ明細(FA)
                    data = self.get_tfd1_FA()
                    for i in data:
                        result.append(i)
                
                if next == 254:
                    result.append(data)
                    break

            else:
                result.append(data)
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

    def get_tfd1(self):

        no = self.exe.getint1()
        len = self.exe.getint1()
        data = self.exe.get(len)
        datastr = '{}({})'.format(' '.join(data[0]), ''.join(data[1]))
        strdata = '項目番号:{},サイズ:{},データ:{}'.format(no, len, datastr)
        next = self.exe.getint1()
        self.exe.first -= 1

        return (strdata, next)

    def get_tfd1_FA(self):

        result = []
        while True:
            no = self.exe.getint1()
            len = self.exe.getint1()
            data = self.exe.get(len)
            datastr = '{}({})'.format(' '.join(data[0]), ''.join(data[1]))
            result.append('マルチ明細{}:サイズ:{},データ:{}'.format(no, len, datastr))

            next = self.exe.getint1()
            self.exe.first -= 1
            if next > 240:
                if next == 252:
                    logger.debug('マルチ明細終了')
                    # 1バイト進める
                    self.exe.getint1()
                break

        return result