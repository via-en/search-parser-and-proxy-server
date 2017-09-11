from rabbit_tasks import CrawlerTaskFactory

rabbit_config = {
  'username': 'test',
  'password': 'test',
  'host': '79.135.230.130:20672',
  'queue': 'testtesttest2',
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
  'mongoServerName': 'mongodb://79.135.230.130:20707',
  'mongoDataBaseName': 'YandexData',
  'mongoCollectionName': 'Posts',
  'snTag': 'YA',
  'crawlID': 'YA-1234',
  'taskID': '599d84c4f89bca2afc8a2e80',
  'count': 10, #кол-во страниц для поиска
  'search_q': 'пластиковые окна site:avito.ru',
  'size': 2, #глубина вложения для скачивания url
  'proxy': 1, #типа да
  'region': ''
}

# В task могут быть добавлены любые дополнительные поля
# см таблицу выше

# вызов этих методов создаст объект таска и положит его в очередь
task_factory.build(**task).send()
