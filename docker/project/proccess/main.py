import logging.config
import os
import sys

from crawler_base import TaskManager
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from awesome_logging import patch_record_factory

from helper.config import Config
from proccess.make_post_proccess import make_sender
from proccess.proccessing import Process
from mongo_structures.utils import init_connection
from mongo_structures.models import ItemDocument


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'..', 'config')
# logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
#logger = logging.getLogger(__name__)


main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


class SomeTaskManager(TaskManager):
  def __init__(self, config):
    super().__init__(config)

  def _callback(self, task):
    self._logger.debug(task.crawlID)

    params = {'snTag': task.snTag, 'CrawlId': task.crawlID}
    payload = {'text': task.search_q}

    patch_record_factory(sn_tag=task.snTag, version='0.1.1', crawl_id=task.crawlID)
    self._logger.info('start processing', extra={'title': 'Crowling'})
    config = {'service_agent_conf_path': main_config.service_agent_conf_path,
              'mongo': {'host_addr': task.mongoServerName,
                        'db_name': task.mongoDataBaseName,
                        'collection': task.mongoCollectionName
                       }
             }

    process = Process(main_config=config, searcher="https://yandex.ru/", params=params)
    self._logger.info('start processing', extra={'title': 'Crowling'})
    process.create_query(payload, pages=3)
    self._logger.info('end processing', extra={'title': 'Crowling'})
    #  if self._task_factory is not None:
    #    self._task_factory.build(_mongoIDsSerialized=str(mongo_id)).send()
    # make_sender(mongo_id)


conf = {
  'rabbit': {
    'username': main_config.main_proccess.rabbit.username,
    'password': main_config.main_proccess.rabbit.password,
    'host':  main_config.main_proccess.rabbit.host,
    'queue': main_config.main_proccess.rabbit.queue,
    'autodelete': False,
    'durable': True,
    'msecsttl': 0,
    'max_task_respawn': 3
  },
  'db': {
    'DB_PORT': main_config.main_proccess.mongo.port,
    'DB_TABLE_NAMES': {
        'errors': 'errors',
        'inputData': 'inputData',
        'docker': 'docker',
        'users': 'users'
    },
    'DB_NAME': main_config.main_proccess.mongo.database,
    'DB_HOST': main_config.main_proccess.mongo.host
  },
  'redis': {
    'REDIS_URL': main_config.main_proccess.redis.url,
    'REDIS_BRANCH': main_config.main_proccess.redis.branch
  },
  'proxy_url': '',
  'headers_url': '',
  'dev_mode': True
}


if __name__ == 'main':
  tm = SomeTaskManager(conf)
  tm.start_consuming()
