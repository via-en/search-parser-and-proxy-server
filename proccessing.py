from urllib.parse import urlencode, quote_plus
import os, sys
import logging.config
from helper.config import Config
from spider.spider import Spider
from parse.parsing import Parse
from pymongo import MongoClient
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


class Process:
    def __init__(self, main_config, searcher):
        self.main_config = main_config
        self.searcher = searcher
        self._sp = None
        self.main_result = []

    @property
    def sp(self):
        if not self._sp:
            self._sp = Spider(placeFrom=self.searcher, main_config=main_config)
        return self._sp

    def create_query(self, payload, pages=3):

        if pages > 0:
            while True:
                if self.main_result:
                    try:
                        page_next = self.main_result[-1]['pages']['pager']['nextPage']
                        if page_next < pages:
                            payload.update({'p': page_next})
                            self.get_query(payload)
                        else:
                            logger.debug(self.main_result)
                            break
                    except Exception as err:
                        logger.debug(err)
                        logger.debug(self.main_result)
                        break

                else:
                    try:
                        self.get_query(payload)
                    except Exception as err:
                        logger.debug(err)
                        logger.debug(self.main_result)
                        break

        try:
            self.create_records()
        except Exception as err:
            logger.debug(err)

    def create_records(self):

        client = MongoClient(host=self.main_config.mongo.host, port=self.main_config.mongo.port)
        db = client[self.main_config.mongo.database]
        yandex = db.yandex

        for record in self.main_result:
            record['date'] = datetime.datetime.now()
            record_id = yandex.insert_one(record).inserted_id
            logger.debug(record_id)

    def get_query(self, payload):

        url_format = urlencode(payload, quote_via=quote_plus)

        url = "search/?{}".format(url_format)
        try:
            pages_result = self.sp.load(url)
        except Exception as err:
            logger.debug(err)
            raise Exception

        # load firts page from parser
        # pages_result={'document', 'url'}
        parse = Parse(pages_result['document'], config_path=config_path)
        parse.make()
        # parse.result = {'pages', 'data'={'snippet', 'href'}}
        pages_result.update(parse.result)
        self.main_result.append(pages_result)

if __name__ == "__main__":


    payload = {'text': 'пластиковые окна'}
    # payload = {'text': 'пластиковые окна','p':'2'}
    process = Process(main_config=main_config,  searcher="https://yandex.ru/")
    process.create_query(payload, pages=3)


