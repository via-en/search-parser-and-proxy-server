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
import hashlib

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'..', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
#logger = logging.getLogger(__name__)

class Process:
    def __init__(self, main_config, searcher, params):
        self.main_config = main_config
        self.searcher = searcher
        self._sp = None
        self.main_result = []
        self.params = params
        self._logger = logging.getLogger('crawler')

    @property
    def sp(self):
        if not self._sp:
            self._sp = Spider(placeFrom=self.searcher, main_config=self.main_config)
        return self._sp

    def create_query(self, payload, pages=3):

        if pages > 0:
            while True:
                if self.main_result:
                    try:
                        page_next = self.main_result[-1]['pages']['pager']['nextPage']
                        if not (type(page_next) == bool and page_next is False) and page_next < pages:
                            payload.update({'p': page_next})
                            self.get_query(payload)
                        else:
                            #self._logger.debug(self.main_result)
                            break
                    except Exception as err:
                        self._logger.debug(err)
                        #self._logger.debug(self.main_result)
                        break

                else:
                    try:
                        self.get_query(payload)
                    except Exception as err:
                        self._logger.debug(payload)
                        self._logger.debug(err)
                        #self._logger.debug(self.main_result)
                        break

        try:
            self.create_records(payload)
        except Exception as err:
            self._logger.debug(err)

    def create_records(self, payload):

        connection_url = "{}/{}".format(self.main_config['mongo']['host_addr'].rstrip("/"),
                                        self.main_config['mongo']['db_name'])

        init_connection(connection_url)

        for record in self.main_result:
            #self._logger.debug(record['data'])
            for index, d in enumerate(record['data'], 1):
                uniq_id = hashlib.md5((d['href'] + '_' + d['snippet']).encode('utf-8')).hexdigest()
                item = Post()
                item.Sntag = self.params['snTag']
                item.CrawlId = [self.params['CrawlId']]
                item.LoadDate = datetime.datetime.now()
                item.Title = d['title']
                item.Text = d['snippet']
                item.URL = d['href']
                item.ID = uniq_id
                item.HashTags = [payload['text']]
                item.spamWeight = index * (payload.get('p', 0) + 1)
                item.PostType = 1
                item.JSONattachments = ""

                self._logger.debug(item.__dict__)

                if not Post.objects(ID=uniq_id).count():
                    record_id = item.save()
                    self._logger.debug("record saved")

    def get_query(self, payload):

        url_format = urlencode(payload, quote_via=quote_plus)

        url = "search/?{}".format(url_format)
        self._logger.debug(url)
        try:
            pages_result = self.sp.load(url)
            #self._logger.debug(pages_result)
        except Exception as err:
            self._logger.debug(err)
            raise err

        # load firts page from parser
        # pages_result={'document', 'url'}
        parse = Parse(pages_result['document'], config_path=config_path)
        parse.make()
        # parse.result = {'pages', 'data'={'snippet', 'href'}}
        pages_result.update(parse.result)
        self.main_result.append(pages_result)


if __name__ == "__main__":

    conf = Config.setup_main_config(os.path.join(config_path, 'main_local.yml'))
    main_config = {'service_agent_conf_path': conf.service_agent_conf_path,
                                     'mongo': {'host_addr': conf.post_proccess.yandex_task.mongo.host_url,
                                               'db_name': conf.post_proccess.yandex_task.mongo.database,
                                               'collection': conf.post_proccess.yandex_task.mongo.collection
                                               }
                  }

    params = {'snTag': 'YA', 'CrawlId': "YA-1234"}

    payload = {'text': 'пластиковые окна в москве'}

    params = {'snTag': 'YA', 'CrawlId':"YA-1234"}
    process = Process(main_config=main_config,  searcher="https://yandex.ru/", params=params)
    process.create_query(payload, pages=2)


