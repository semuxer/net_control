import re
from datetime import datetime

from defaults import *


class parser():
    def __init__(self, parse_str, reg_patern=r"^(?P<date>[^|]*)\|(?P<level>[^|]*)\|((?P<to>.*)\:(?P<ip>.*)|(?P<message>.*))$"
                 ):
        pattern = re.compile(reg_patern)
        match = pattern.search(parse_str)

        if match:
            self.results = match.groupdict()
        else:
            self.results = None

    def getresults(self):
        if self.results:
            return self.results


if __name__ == "__main__":
    txt = "2024-02-27 13:42:20 | SUCCESS | Відновлено зв'язок з: 8.8.8.8"
    mth = parser(txt)
    print(mth.getresults().get('to'))
