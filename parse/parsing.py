import os, sys
from lxml import etree
from  lxml.etree import ElementTree
from lxml.html.clean import Cleaner
import logging.config
from io import StringIO, BytesIO
from collections import namedtuple

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(os.path.join(os.path.join(CURRENT_DIR,'..','config'), 'logging.conf'))
logger = logging.getLogger(__name__)

from lxml.html.soupparser import fromstring
from helper.config import Config

class Parse:
    def __init__(self, buffer, config_path=None):
        logger.debug("parse")
        self.buffer = buffer
        self.config = Config.setup_main_config(os.path.join(config_path, 'yandex.yml'))
        self.result = []
        self._cleaner = None

    def make(self):
        tree = fromstring(self.buffer, features="html.parser")
        matches = tree.xpath(self.config.li)
        for li in matches:
            snippet = etree.tostring(self.cleaner.clean_html(li), method="xml", encoding="UTF-8").decode()
            reffer_tree = fromstring(etree.tostring(li, method="xml", encoding="UTF-8").decode())
            self.result.append(snippet)

    @property
    def cleaner(self):
        if not self._cleaner:
            cleaner_i = Cleaner()
            cleaner_i.javascript = True
            cleaner_i.style = True
            cleaner_i.meta = True
            cleaner_i.safe_attrs_only = True
            cleaner_i.remove_tags = ['div', 'i', 'span', 'b']
            cleaner_i.safe_attrs = ['href']

            self._cleaner = cleaner_i

        return self._cleaner


if __name__ == "__main__":

    buffer = open("result0.html", "r", encoding='UTF-8')
    parse = Parse(buffer, config_path=os.path.join(CURRENT_DIR,'..','config'))
    parse.make()
    logger.debug(parse.result)