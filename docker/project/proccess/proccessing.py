import datetime
import logging.config
import os
import sys
from urllib.parse import urlencode, quote_plus

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from helper.config import Config
from parse.parsing import Parse
from spider.spider import Spider
from mongo_structures.utils import init_connection
from mongo_structures.models import Post


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'..', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)

class Process:
    def __init__(self, main_config, searcher, params):
        self.main_config = main_config
        self.searcher = searcher
        self._sp = None
        self.main_result = []
        self.params = params

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
            self.create_records(payload)
        except Exception as err:
            logger.debug(err)

    def create_records(self, payload):

        connection_url = "{}/{}".format(main_config.post_proccess.yandex_task.mongo.host_url,
                                        main_config.post_proccess.yandex_task.mongo.database)

        init_connection(connection_url)

        for record in self.main_result:
            for index, d in enumerate(record['data'], 1):
                item = Post()
                item.Sntag = params['snTag']
                item.CrawlId = [params['CrawlId']]
                item.LoadDate = datetime.datetime.now()
                item.Title = d['snippet']
                item.URL = d['href']
                item.ID = d['href']
                item.HashTags = [payload['text']]
                item.spamWeight = index * (payload.get('p', 0) + 1)
                item.PostType = 1
                item.JSONattachments = ""

                if not Post.objects(ID=d['href']).count():
                    record_id = item.save()
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

    main_config = Config.setup_main_config(os.path.join(config_path, 'main_local.yml'))

    params = {'snTag': 'YA', 'CrawlId': "YA-1234"}

    payload = {'text': 'пластиковые окна в москве'}

    params = {'snTag': 'YA', 'CrawlId':"YA-1234"}
    process = Process(main_config=main_config,  searcher="https://yandex.ru/", params=params)
    process.create_query(payload, pages=2)


