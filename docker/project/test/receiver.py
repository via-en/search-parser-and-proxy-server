import logging.config
import os
import sys

from crawler_base import TaskManager
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from helper.config import Config


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'../', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


class SomeTaskManager(TaskManager):
  def __init__(self, config):
    super().__init__(config)

  def _callback(self, task):
    logger.debug(task.crawlID)
    # if self._task_factory is not None:
    #   self._task_factory.build(_mongoIDsSerialized=str(mongo_id)).send()


config = {
  'rabbit': {
    'username': 'test',
    'password': 'test',
    'host': '172.17.100.169:5672',
    'queue': 'testtesttest',
    'autodelete': False,
    'durable': True,
    'msecsttl': 0,
    'max_task_respawn': 3
  },
  'db': {
    'DB_PORT': '20707',
    'DB_TABLE_NAMES': {
        'errors': 'errors',
        'inputData': 'inputData',
        'docker': 'docker',
        'users': 'users'
    },
    'DB_NAME': 'YandexData',
    'DB_HOST': '172.17.100.168'
  },
  'redis': {
    'REDIS_URL': 'redis://:@172.17.100.169:6379/0',
    'REDIS_BRANCH': 'TestTest'
  },
  'proxy_url': '',
  'headers_url': '',
  'dev_mode': True
}

tm = SomeTaskManager(config)
tm.start_consuming()
