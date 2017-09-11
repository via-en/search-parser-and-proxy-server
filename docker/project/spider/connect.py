
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import randint
import os, sys
import logging.config
from datetime import date
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import proxy.pproxy

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, '..', 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))

from pyvirtualdisplay import Display

#logger = logging.getLogger(__name__)


class ConnectManager:
    def __init__(self, path_user_agents, service_log):
        self.count = 0
        self.freeDrivers = []
        self.drivers = []
        self.headers = []
        self.service_log = service_log
        fileAgents = open(path_user_agents)
        self._logger = logging.getLogger('crawler')
        for agent in fileAgents:
            self.headers.append(agent)
        self.display = Display(visible=0, size=(1920, 1080)).start()

    def erase(self, driver):
        self.freeDrivers.append(self.drivers.index(driver))

    def erase_all(self):
        self.freeDrivers = range(self.count)

    def create(self):
        try:
            prx = proxy.pproxy.give_proxy().partition('@')
        except Exception as err:
            self._logger.debug(err)
            raise err

        try:
            service_args = [
                '--proxy={}'.format(prx[2]),
                '--proxy-type=https',
                '--proxy-auth={}'.format(prx[0]),
            ]
        except AttributeError:
            self._logger.debug("error while getting proxy")
            service_args = [
                '--proxy={}'.format(prx),
                '--proxy-type=https',
            ]

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = self.headers[randint(0, len(self.headers) - 1)]

        #dcap["phantomjs.page.settings.userAgent"] = 'Lynx/2.8.9dev.8 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/3.4.9'
        #
        dcap['phantomjs.page.customHeaders.Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        #dcap['phantomjs.page.customHeaders.Accept-Encoding'] = 'gzip, deflate, br'
        dcap['phantomjs.page.customHeaders.Accept-Charset'] = 'utf-8'
        dcap['phantomjs.page.customHeaders.Accept-Language'] = 'ru,en;q=0.8'
        dcap['phantomjs.page.customHeaders.X-Requested-With'] = 'XMLHttpRequest'
        dcap['phantomjs.page.customHeaders.Connection'] = 'Keep-Alive'
        dcap['phantomjs.page.customHeaders.Host'] = 'yandex.ru'

        service_log_path = os.path.join(self.service_log, 'ghostdriver.log.' + str(date.today()))

        driver = webdriver.PhantomJS(service_args=service_args, desired_capabilities=dcap, service_log_path=service_log_path)
        # driver = webdriver.PhantomJS(desired_capabilities=dcap,
        #                              service_log_path=service_log_path) #without proxy
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)

        return driver

    def get_driver(self):

        if self.freeDrivers == []:
            self.drivers.append(self.create())
            self.count += 1

            return self.drivers[-1]

        idx = self.freeDrivers.pop()
        return self.drivers[idx]

    def restart(self, driver):
        num = self.drivers.index(driver)

        self.drivers[num].close()
        self.drivers[num] = self.create()

        return self.drivers[num]


if __name__ == "__main__":

    manager = ConnectManager(path_user_agents=os.path.join(config_path, "userAgents.txt"))