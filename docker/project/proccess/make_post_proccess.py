import logging.config
import os
import sys
from rabbit_tasks import TextParseTaskFactory

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from helper.config import Config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'../', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)

main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))


rabbit_conf = {
  "host": main_config.post_proccess.rabbit.host,
  "queue": main_config.post_proccess.rabbit.queue,
  "username": main_config.post_proccess.rabbit.username,
  "password": main_config.post_proccess.rabbit.password,
  "autodelete": False,
  "durable": True,
  "msecsttl": 0
}

task_config = {
  "priority": 5,
  "mongoServerName": main_config.post_proccess.yandex_task.mongo.host_url,
  "mongoDataBaseName": main_config.post_proccess.yandex_task.mongo.database,
  "mongoCollectionName": main_config.post_proccess.yandex_task.mongo.collection,
  "morphologyEngine": 1,
  "syntaxEngine": 1,
  "sentimentEngine": 1,
  "langDetectEngine": 1,
  "indexationEngine": 1,
  "rubricationEngine": 1,
  "annotationEngine": 1,
  "wawesEngine": 1,
  "geotagEngine": 1,
  "artificialEngine": 1,
  "specialQueries": [
    "aaa",
    "bbb"
  ],
  "language": 0
}

def make_sender(mongo_id):
    task_factory = TextParseTaskFactory(rabbit_conf, task_config)
    #task1 = task_factory.build(_mongoIDsSerialized='599d84c4f89bca2afc8a2e80')
    task = task_factory.build(_mongoIDsSerialized=str(mongo_id))
    task.send()
