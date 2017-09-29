import unittest
import json
import os, sys
import logging.config
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_DIR, 'logging.conf'))
logger = logging.getLogger(__name__)
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from parse.parsing import Parse


logger = logging.getLogger(__name__)


class TestParsing(unittest.TestCase):

    def test_middle_page(self):

        origin = {
            'pages': {'pager': {'id': 'pager', 'nextPage': 4, 'prevPage': 2}},
            'data': [
                {'snippet': '<div><div><h2><a href="http://Okna-Veka.info/">«Окна Века» — пластиковые окна</a></h2><div><div><a href="http://Okna-Veka.info/">Okna-Veka.info</a></div><div><div><a href="http://hghltd.yandex.net/yandbtm?fmode=inject&amp;url=http%3A%2F%2FOkna-Veka.info%2F&amp;tld=ru&amp;lang=ru&amp;la=1505454848&amp;tm=1505718146&amp;text=%D0%BF%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0&amp;l10n=ru&amp;mime=html&amp;sign=3379a71668167ba0b485e7cd42ee9c22&amp;keyno=0">Сохранённая копия</a><a href="/search/?lr=213&amp;msid=1505715928.06326.22884.27682&amp;text=%D0%BF%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0&amp;noreask=1&amp;site=Okna-Veka.info">Показать ещё с сайта</a>Пожаловаться</div></div></div><div><div>Производство и монтаж пластиковых окон; остекление балконов и <wbr/>лоджий. Цены. Онлайн-калькулятор стоимости. Портфолио. Форма для <wbr/>вызова замерщика.<br/></div></div></div></div>',
                 'href': 'http://Okna-Veka.info/',
                 'title': '«Окна Века» — пластиковые окна',
                 'text': '«Окна Века» — пластиковые окна\nOkna-Veka.info\nСохранённая копия\nПоказать ещё с сайта\nПожаловаться\nПроизводство и монтаж пластиковых окон; остекление балконов и \nлоджий. Цены. Онлайн-калькулятор стоимости. Портфолио. Форма для \nвызова замерщика.'
                 }
            ]
        }

        buffer = open(os.path.join(CURRENT_DIR, "files", "result3.html"), "r", encoding='UTF-8')
        parse = Parse(buffer, config_path=os.path.join(CURRENT_DIR, '..', 'config'))
        parse.make()
        buffer.close()
        self.assertEqual(parse.result['data'][0], origin['data'][0])

    def test_first_page(self):

        origin = {
            'pages': {'pager': {'id': 'pager', 'nextPage': 1, 'prevPage': False}},
            'data': [
                {'snippet': '<div><div><h2><div>1</div><a href="https://www.mosokna.ru/ceny-plastikovye-okna/">Пластиковые окна - цены и размеры с установкой...</a></h2><div><div><a href="https://www.mosokna.ru/">mosokna.ru</a>›<a href="https://www.mosokna.ru/ceny-plastikovye-okna/">ceny-plastikovye-okna/</a></div><div><div><a href="https://hghltd.yandex.net/yandbtm?fmode=inject&amp;url=https%3A%2F%2Fwww.mosokna.ru%2Fceny-plastikovye-okna%2F&amp;tld=ru&amp;lang=ru&amp;la=1505431040&amp;tm=1505727749&amp;text=%D0%BF%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0&amp;l10n=ru&amp;mime=html&amp;sign=185a9eb5e3b2b786fd85af96dae3deff&amp;keyno=0">Сохранённая копия</a><a href="/search/?text=%D0%BF%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0&amp;lr=213&amp;noreask=1&amp;site=www.mosokna.ru">Показать ещё с сайта</a>Пожаловаться</div></div></div><div><div>Пластиковые окна: цены с установкой. В Москве нет ни одного дома, <wbr/>где бы не были установлены Московские окна.</div></div></div></div>',
                 'href': 'https://www.mosokna.ru/ceny-plastikovye-okna/',
                 'title': 'Пластиковые окна - цены и размеры с установкой...',
                 'text': "1\nПластиковые окна - цены и размеры с установкой...\nmosokna.ru\n›\nceny-plastikovye-okna/\nСохранённая копия\nПоказать ещё с сайта\nПожаловаться\nПластиковые окна: цены с установкой. В Москве нет ни одного дома, \nгде бы не были установлены Московские окна."}
            ]
        }

        buffer = open(os.path.join(CURRENT_DIR, "files", "result0.html"), "r", encoding='UTF-8')
        parse = Parse(buffer, config_path=os.path.join(CURRENT_DIR, '..', 'config'))
        parse.make()
        buffer.close()
        self.assertEqual(parse.result['data'][0], origin['data'][0])


if __name__ == '__main__':
    unittest.main()