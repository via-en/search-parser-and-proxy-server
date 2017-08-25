import logging.config
import os
import sys
from urllib.parse import urlencode, quote_plus

from helper.config import Config

from spider.connect import ConnectManager

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'..', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


class Spider(object):
    def __init__(self, placeFrom, main_config):

        self.placeFrom = placeFrom
        self.manager = ConnectManager(path_user_agents=os.path.join(config_path, "userAgents.txt"), service_log=main_config.service_agent_conf_path)

    def load(self, url):
        data = {'url': None, 'document': None}

        driver = self.manager.driver()
        driver.get(self.placeFrom + url)
        data['url'] = url
        data['document'] = driver.page_source
        driver.quit()

        return data


if __name__ == "__main__":

    fromX = "https://yandex.ru/"
    toX = "/test-projects-proxy/result"
    # payload = {'q': 'юбка'}
    payload = {'text': 'пластиковые окна'}
    result = urlencode(payload, quote_via=quote_plus)

    listUrls = ["search/?{}".format(result)]
    print(listUrls)
    main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))
    sp = Spider(placeFrom=fromX, main_config=main_config)
    result = sp.load(listUrls)
