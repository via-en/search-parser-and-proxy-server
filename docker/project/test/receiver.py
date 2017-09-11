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
# logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
#logger = logging.getLogger(__name__)


main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


config = {
  'rabbit': {
    'username': 'test',
    'password': 'test',
    'host': '79.135.230.130:20672',
    'queue': 'testtesttest2',
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
    'DB_HOST': '79.135.230.130'
  },
  'redis': {
    'REDIS_URL': 'redis://:@79.135.230.130:20379/0',
    'REDIS_BRANCH': 'TestTest'
  },
  'proxy_url': '',
  'headers_url': '',
  'dev_mode': True,
  'logging': {
        'names': 'yandex',
        'level': 0,
        'file_path': '/usr/src/app/project/logs/test.log',
        'elastic_url': ''
  }
}


if __name__ == '__main__':
    tm = SomeTaskManager(config)
    tm.start_consuming()
