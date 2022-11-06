from logging import getLogger

logger = getLogger(__name__)

class execute():
    def __init__(self, file):
        self.file = file

    def execute(self, first, last):
        print(__name__)
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
