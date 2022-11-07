from logging import getLogger
from tool.Execute import execute
from tool.CiiHeader import cii_header
from tool.CiiTrailer import cii_trailer
import unicodedata

logger = getLogger(__name__)


class analyze():
    def __init__(self, file):
        self.file = file
        self.exe = execute(file)

    def head(self):
        ciihead = cii_header(self.exe)
        ciihead.print()

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
        ciitrail = cii_trailer(self.exe)
        ciitrail.print()

