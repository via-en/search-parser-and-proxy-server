import datetime
import logging.config
import os
import sys
from urllib.parse import urlencode, quote_plus

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from parse.parsing import Parse
from spider.spider import Spider
from mongo_structures.utils import init_connection
from mongo_structures.models import Post
import hashlib

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, '..', 'config')


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
                            break
                    except Exception as err:
                        self._logger.debug(err)
                        break

                else:
                    try:
                        self.get_query(payload)
                    except Exception as err:
                        self._logger.debug(payload)
                        self._logger.debug(err)
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
            for index, d in enumerate(record['data'], 1):
                uniq_id = hashlib.md5((d['href'] + '_' + d['snippet']).encode('utf-8')).hexdigest()
                if not Post.objects(ID=uniq_id).count():
                    item = Post()
                    item.Sntag = self.params['snTag']
                    if self.params['workflowID']:
                        item.WorkflowId = self.params['workflowID']

                    item.CrawlId = [self.params['CrawlId']]
                    item.LoadDate = datetime.datetime.now()
                    item.Title = d['title']
                    item.Text = d['text']
                    item.URL = d['href']
                    item.ID = uniq_id
                    item.HashTags = [payload['text']]
                    item.spamWeight = index * (payload.get('p', 0) + 1)
                    item.PostType = 1
                    self._logger.debug(item.__dict__)
                    item.save()
                    self._logger.debug("record saved with ID {}".format(uniq_id))
                else:
                    Post.objects(ID=uniq_id).update_one(add_to_set__CrawlId=self.params['CrawlId'])
                    if self.params['workflowID']:
                        Post.objects(ID=uniq_id).update_one(add_to_set__CrawlId=self.params['CrawlId'],
                                                            add_to_set__WorkflowId=self.params['workflowID'])
                    else:
                        Post.objects(ID=uniq_id).update_one(add_to_set__CrawlId=self.params['CrawlId'])

                    self._logger.debug("record update with ID {}".format(uniq_id))

    def get_query(self, payload):

        url_format = urlencode(payload, quote_via=quote_plus)

        url = "search/?{}".format(url_format)
        pages_result = {}

        try:
            if self.sp:
                pages_result = self.sp.load(url)
        except Exception:
            self._logger.error("Can't load page {} ".format(url))
        else:
            if pages_result:
                parse = Parse(pages_result['document'], config_path=config_path)
                parse.make()
                pages_result.update(parse.result)
                self.main_result.append(pages_result)


