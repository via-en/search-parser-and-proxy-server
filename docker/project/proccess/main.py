import os
import sys

from crawler_base import TaskManager
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from awesome_logging import patch_record_factory

from helper.config import Config
from proccess.proccessing import Process

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, '..', 'config')

main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


class SomeTaskManager(TaskManager):

  def __init__(self, config):
    super().__init__(config)

  def _callback(self, task):
    self._logger.debug(task.crawlID)

    params = {'snTag': task.snTag, 'CrawlId': task.crawlID, 'workflowID': task.workflowID}

    patch_record_factory(sn_tag=task.snTag, version='0.1.1', crawl_id=task.crawlID)
    self._logger.info('start processing', extra={'title': 'Crowling'})
    config = {'service_agent_conf_path': main_config.service_agent_conf_path,
              'mongo': {'host_addr': task.mongoServerName,
                        'db_name': task.mongoDataBaseName,
                        'collection': task.mongoCollectionName
                       }
             }
    for query in task.search_q:
        payload = {'text': query}
        process = Process(main_config=config, searcher="https://yandex.ru/", params=params)
        self._logger.info('start processing', extra={'title': 'Crowling'})
        process.create_query(payload, pages=task.count)
        self._logger.info('end processing', extra={'title': 'Crowling'})
