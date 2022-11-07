from logging import getLogger
from tool.Execute import execute
from tool.CiiHeader import cii_header
from tool.CiiTrailer import cii_trailer
from tool.CiiMessage import cii_message
import unicodedata

logger = getLogger(__name__)


class analyze():
    def __init__(self, file):
        self.file = file
        self.exe = execute(file)

    def head(self):
        ciihead = cii_header(self.exe)
        ciihead.print()

    def message(self):
        ciimessage = cii_message(self.exe)
        ciimessage.print()

    def trailer(self):
        ciitrail = cii_trailer(self.exe)
        ciitrail.print()

