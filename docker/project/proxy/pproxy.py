import requests
import os
import lxml.html as html
import time
import logging

headers = {
    'User-Agent': 'Lynx/2.8.9dev.8 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/3.4.9',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'Keep-Alive',
    'Host': 'yandex.ru'
    }

url = 'https://yandex.ru/search/?text=qwerty&lr=213'
download_url = 'http://api.foxtools.ru/v2/Proxy.txt' \
               '?cp=UTF-8&lang=Auto&type=HTTPS&available=Yes&free=Yes&uptime=5&limit='

proxy_list = []
proxy_list_cleaned = []
scan_dir = ''
scan_file = '../proxy/proxies.txt'
cleaned_file = '../proxy/proxies_cleaned.txt'
log_file = '../proxy/log.txt'


def import_file():
    global proxy_list

    proxy_list = [line.rstrip('\n') for line in open(os.path.join(scan_dir, scan_file), 'r')]


def export_file():
    with open(cleaned_file, 'w') as file:
        for line in proxy_list_cleaned:
            file.write('%s\n' % line)


def update_cleaned_file():
    global cleaned_file
    try:
        file = open(cleaned_file).readlines()
        line = file.pop(0)
        with open(cleaned_file, 'w') as f:
            f.writelines(file)
            f.write(line)
    except Exception:
        pass


def check_captcha(htmlr):
    page = html.fromstring(htmlr)
    if page.cssselect('.form__captcha') or htmlr[0] == '{':
        return False
    return True


def check_proxy(proxy):
    proxy_dict = {
        "https": "https://" + proxy,
    }
    logger = logging.getLogger('crawler')
    try:
        r = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
        if (r.status_code == 200) and (check_captcha(r.text)):
            return True
        else:
            return False
    except Exception as err:
        logger.debug(err)
        return False


def check_proxies():
    global proxy_list
    global proxy_list_cleaned

    import_file()

    file = open(log_file, 'w')

    for proxy in proxy_list:
        if check_proxy(proxy):
            file.write(proxy + ' ok\n')
            proxy_list_cleaned.append(proxy.rstrip('https://'))
        else:
            file.write(proxy + ' not ok\n')
        time.sleep(2)

    file.close()
    export_file()


def give_proxy():
    logger = logging.getLogger('crawler')
    try:
        file = open(cleaned_file, 'r')
        for i in range(0, sum(1 for line in open(cleaned_file, 'r'))):
            proxy = file.readline().rstrip('\n')
            if check_proxy(proxy):
                update_cleaned_file()
                return proxy
        file.close()
    except Exception as err:
        logger.debug(err)
    return None


def download_proxy(amount=100):
    r = requests.get(download_url + str(amount), headers=headers, timeout=10)
    with open(scan_file, 'w') as f:
        f.writelines(r.text)
