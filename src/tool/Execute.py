from logging import getLogger

logger = getLogger(__name__)

class execute():
    def __init__(self, file, first=0):
        self.file = file
        self.first = first

    def execute(self, first, last):
        logger.debug(self.file)
        with open(self.file, 'br') as f:
            f.seek(first)
            data = f.read(last)
            result_b = []
            result_c = []
            for i in data:
                result_b.append(hex(i))
                result_c.append(chr(i))

            logger.debug('b:{}'.format(result_b))
            logger.debug('c:{}'.format(result_c))
            return (result_b, result_c)

    def get(self, size):
        result = self.execute(self.first, size)
        self.first += size
        return result

    def getint2(self):

        with open(self.file, 'br') as f:
            f.seek(self.first)
            data = f.read(2)

        self.first += 2
        return int.from_bytes(data, 'big')

    def getint1(self):

        with open(self.file, 'br') as f:
            f.seek(self.first)
            data = f.read(1)

        self.first += 1
        return int.from_bytes(data, 'big')