import os, sys
from lxml import etree
from  lxml.etree import ElementTree
from lxml.html.clean import Cleaner
import logging.config
from io import StringIO, BytesIO
from collections import namedtuple
import json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(os.path.join(os.path.join(CURRENT_DIR,'..','config'), 'logging.conf'))
logger = logging.getLogger(__name__)

from lxml.html.soupparser import fromstring
from helper.config import Config


class Parse:

    def __init__(self, buffer, config_path=None):
        self.buffer = buffer
        self.config = Config.setup_main_config(os.path.join(config_path, 'yandex.yml'))
        self.result = []
        self._cleaner = None

    def make(self):
        tree = fromstring(self.buffer, features="html.parser")
        matches = tree.xpath(self.config.ul)
        ul = matches[0]
        lis = ul.xpath(self.config.li)
        data = {}
        data['pages'] = json.loads(tree.xpath(self.config.pages)[0])
        data['data'] = []

        for li in lis:
            cleaner = self.cleaner_li()
            tmp = {}
            tmp['snippet'] = etree.tostring(cleaner.clean_html(li), method="xml", encoding="UTF-8").decode()
            tree_temp = fromstring(tmp['snippet'], features="html.parser")
            href = tree_temp.xpath(self.config.href)
            tmp['href'] = href[0]

            data['data'].append(tmp)

        self.result = data

    def cleaner_li(self):
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        cleaner.meta = True
        cleaner.safe_attrs_only = True
        cleaner.remove_tags = ['i', 'span', 'b', 'li']
        cleaner.safe_attrs = ['href']

        return cleaner


if __name__ == "__main__":

    buffer = open("result0.html", "r", encoding='UTF-8')
    parse = Parse(buffer, config_path=os.path.join(CURRENT_DIR,'..','config'))
    parse.make()
    logger.debug(parse.result)