from rabbit_tasks import CrawlerTaskFactory

rabbit_config = {
  'username': 'test',
  'password': 'test',
  'host': '172.17.100.169:5672',
  'queue': 'testtesttest',
  'autodelete': False,
  'durable': True,
  'msecsttl': 0,
  'max_task_respawn': 3
}

task_base = {
  'priority': 5
}

task_factory = CrawlerTaskFactory(rabbit_config, task_base)

# Отправка тасков
# обязательные поля
task = {
  'mongoServerName': 'mongodb://172.17.100.168:2375',
  'mongoDataBaseName': 'YandexData',
  'mongoCollectionName': 'Posts',
  'snTag': 'YA',
  'crawlID': 'YA-1234',
  'taskID': '599d84c4f89bca2afc8a2e80',
}

# В task могут быть добавлены любые дополнительные поля
# см таблицу выше

# вызов этих методов создаст объект таска и положит его в очередь
task_factory.build(**task).send()
