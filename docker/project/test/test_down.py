import logging.config
import os
import sys

from crawler_base import TaskManager
from crawler_base.run import main

from docker.project.helper import Config

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)

main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))

config = {
  "mongoServerName": "mongodb://127.0.0.1:27017/",
  "mongoDataBaseName": "Twitter",
  "mongoCollectionName": "Posts",
  "snTag": "",
  "crawlID": "",

}

class SomeTaskManager(TaskManager):
  def __init__(self, config):
    super().__init__(config)

  def _callback(self, task):
    logger.debug(task.crawlID)

    # if self._task_factory is not None:
    #   self._task_factory.build(_mongoIDsSerialized=str(mongo_id)).send()

if __name__ == '__main__':
  main(SomeTaskManager)
