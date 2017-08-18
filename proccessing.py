from urllib.parse import urlencode, quote_plus
import os, sys
import logging.config
from helper.config import Config
from spider.spider import Spider
from parse.parsing import Parse

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


fromX = "https://yandex.ru/"
toX = "/test-projects-proxy/result"
payload = {'text': 'пластиковые окна'}
#payload = {'text': 'пластиковые окна','p':'2'}
result = urlencode(payload, quote_via=quote_plus)

listUrls = ["search/?{}".format(result)]
main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))
sp = Spider(placeFrom=fromX, placeTo=toX, main_config=main_config)
result = sp.load(listUrls)
logger.debug(result)
for key, value in result.items():
    parse = Parse(value, config_path=config_path)
    parse.make()
    logger.debug(parse.result)