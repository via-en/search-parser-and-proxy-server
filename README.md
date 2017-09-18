## Обязательные входные параметры для создания задачи: 

 - 'mongoServerName': 'mongodb://172.17.100.169:28015',
 - 'mongoDataBaseName': 'YandexData', # бд
 - 'mongoCollectionName': 'Posts', # коллекция
 - 'snTag': 'YA',
 - 'crawlID': 'YA-1234',#идентификатор сборщика
 - 'taskID': '599d84c4f89bca2afc8a2e80', #идентификатор задачи
 - 'count': 10, #кол-во страниц для поиска 
 - 'search_q': 'пластиковые окна site:avito.ru', #поисковой запрос
 - 'size': 2, # не используется
 - 'proxy': 1, #использоваение прокси
 - 'region': '' #указывается идентификатор региона

## Результат - объект коллекции Posts c параметрами:

- 'Sntag':'YA',
- 'CrawlId':'YA-1234',
- 'LoadDate': дата,
- 'Title':заголовок сниппета,
- 'text': сниппет
- 'URL':главная ссылка сниппета,
- 'ID': из md5(главная ссылка сниппета + сниппет) преобразуется в hex,
- 'HashTags': поисковой запрос,
- 'spamWeight': порядковый номер сниппета,
- 'PostType': 1,
- 'JSONattachments':''(не используется)
