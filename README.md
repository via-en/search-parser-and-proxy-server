Пример создания задачи в "ручном" виде, для 

task = {
  'mongoServerName': 'mongodb://172.17.100.169:28015',
  'mongoDataBaseName': 'YandexData',
  'mongoCollectionName': 'Posts',
  'snTag': 'YA',
  'crawlID': 'YA-1234',
  'taskID': '599d84c4f89bca2afc8a2e80',
  'count': 10, #глубина вложения для скачивания snippet(не используется)
  'search_q': 'пластиковые окна site:avito.ru', #поисковой запрос
  'size': 2, #кол-во страниц для поиска 
  'proxy': 1, #использоваение прокси
  'region': '' #указывается идентификатор региона
}

# вызов этих методов создаст объект таска и положит его в очередь

task_factory.build(**task).send()


На выходе получается, объект Post c параметрами( для яндекса):

Sntag # 'YA'
CrawlId # 'YA-1234'
LoadDate # дата 
Title # сниппет
URL # главная ссылка сниппета
ID # из md5(главная ссылка сниппета + сниппет) преобразуется в hex
HashTags #поисковой запрос
spamWeight #порядковый номер сниппета
PostType # 1
JSONattachments # ''(не используется)
