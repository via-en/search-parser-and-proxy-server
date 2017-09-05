import logging.config
import os
import sys

from crawler_base import TaskManager
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from helper.config import Config

sys.path.append("/usr/src/app/")
sys.path.append("/usr/src/app/project")
from proccess.main import SomeTaskManager

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'../', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


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


if __name__ == '__main__':
    tm = SomeTaskManager(config)
    tm.start_consuming()
