import logging.config
import os
import sys

from crawler_base import TaskManager
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))


from helper.config import Config
from proccess.make_post_proccess import make_sender
from proccess.proccessing import Process
from mongo_structures.utils import init_connection
from mongo_structures.models import ItemDocument


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'..', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


class SomeTaskManager(TaskManager):
  def __init__(self, config):
    super().__init__(config)

  def _callback(self, task):
    logger.debug(task.crawlID)

    payload = {'text': 'пластиковые окна'}
    process = Process(main_config=main_config, searcher="https://yandex.ru/")
    process.create_query(payload, pages=3)

    #  if self._task_factory is not None:
    #    self._task_factory.build(_mongoIDsSerialized=str(mongo_id)).send()
    # make_sender(mongo_id)


config = {
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

tm = SomeTaskManager(config)
tm.start_consuming()
