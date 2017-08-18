from urllib.parse import urlencode, quote_plus
import os, sys
import logging.config
from spider.connect import ConnectManager
from helper.config import Config

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'..', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


class Spider(object):
    def __init__(self, placeFrom, placeTo, main_config):

        self.placeFrom = placeFrom
        self.placeTo = placeTo
        self.manager = ConnectManager(path_user_agents=os.path.join(config_path, "userAgents.txt"), service_log=main_config.service_agent_conf_path)

    def load(self, listUrls):

        result = {}

        for url in listUrls:

            driver = self.manager.driver()
            driver.get(self.placeFrom + url)
            result[url] = driver.page_source
            driver.quit()

        return result


if __name__ == "__main__":

    fromX = "https://yandex.ru/"
    toX = "/test-projects-proxy/result"
    # payload = {'q': 'юбка'}
    payload = {'text': 'пластиковые окна'}
    result = urlencode(payload, quote_via=quote_plus)

    listUrls = ["search/?{}".format(result)]
    print(listUrls)
    main_config = Config.setup_main_config(os.path.join(config_path, 'main.yml'))
    sp = Spider(placeFrom=fromX, placeTo=toX, main_config=main_config)
    result = sp.load(listUrls)
