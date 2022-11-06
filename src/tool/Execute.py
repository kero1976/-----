from logging import getLogger

logger = getLogger(__name__)

class execute():
    def __init__(self, file):
        self.file = file

    def execute(self):
        logger.debug(self.file)
        with open(self.file) as f:
            data = f.read(2)
            logger.debug(data)

        logger.debug('END')