import datetime
import logging
import re
import requests

from .html_parser import HTMLParser

class SCNClient(object):
    DECIMAL_REGEXP = re.compile("\d+,\d+")
    INT_REGEXP = re.compile("\d+")

    def __init__(self, url='http://www.scn.put.poznan.pl/main.php'):
        self.log = logging.getLogger('scnmonitor.SCNClient')
        self.url = url
        self.updated = None
        self.download = 0
        self.upload = 0
        self.total = 0
        self.percentage = 0

    def check(self):
        url = "{}?view=transfer".format(self.url)
        self.log.info("Fetching usage data from %s...", url)
        response = requests.get(url)
        html = response.text

        parser = HTMLParser()
        parser.feed(html)

        self.download = self.extract_decimal(parser.output['download'])
        self.upload = self.extract_decimal(parser.output['upload'])
        self.total = self.extract_decimal(parser.output['total'])
        self.percentage = self.extract_int(parser.output['percentage'])

        self.updated = datetime.datetime.now()
        self.log.info("Information downloaded successfully")

    def extract_decimal(self, text):
        self.log.debug("Scanning the string '%s' for a decimal", text)
        try:
            number = self.DECIMAL_REGEXP.search(text).group(0)
            return float(number.replace(',', '.'))
        except (AttributeError, IndexError, ValueError):
            self.log.exception("Failed to match a decimal!")

    def extract_int(self, text):
        self.log.debug("Scanning the string '%s' for an integer", text)
        try:
            number = self.INT_REGEXP.search(text).group(0)
            return int(number)
        except (AttributeError, IndexError, ValueError):
            self.log.exception("Failed to match an integer!")
