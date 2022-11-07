from logging import getLogger
import unicodedata

logger = getLogger(__name__)


class cii_message2():

    def __init__(self, exe):
        self.exe = exe

    def print(self):
        datas = self.get()
        for i in datas:
            print(i)
            
    def get(self):
        return self.control()

    def control(self):

        result = []
        (data, size) = self.message_group()
        for i in data:
            result.append(i)
        tfd = self.get_tfd_manager()
        for i in tfd:
            result.append(i)
        buff = (self.exe.first % 251)
        buff_size = 251 - buff
        logger.info('空白サイズ:{}'.format(buff_size))
        result.append(self.format('空白', buff_size))
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