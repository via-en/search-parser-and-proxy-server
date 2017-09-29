from lxml.html.soupparser import fromstring
from lxml import etree
from lxml.etree import strip_tags
from lxml.html.clean import Cleaner, clean_html
import os,sys
import logging.config
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_DIR, 'logging.conf'))
logger = logging.getLogger(__name__)

text = '<div><div><h2><a href="http://Okna-Veka.info/">«Окна Века» — пластиковые окна</a></h2><div><div><a href="http://Okna-Veka.info/">Okna-Veka.info</a></div><div><div><a href="http://hghltd.yandex.net/yandbtm?fmode=inject&amp;url=http%3A%2F%2FOkna-Veka.info%2F&amp;tld=ru&amp;lang=ru&amp;la=1505454848&amp;tm=1505718146&amp;text=%D0%BF%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0&amp;l10n=ru&amp;mime=html&amp;sign=3379a71668167ba0b485e7cd42ee9c22&amp;keyno=0">Сохранённая копия</a><a href="/search/?lr=213&amp;msid=1505715928.06326.22884.27682&amp;text=%D0%BF%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0&amp;noreask=1&amp;site=Okna-Veka.info">Показать ещё с сайта</a>Пожаловаться</div></div></div><div><div>Производство и монтаж пластиковых окон; остекление балконов и <wbr/>лоджий. Цены. Онлайн-калькулятор стоимости. Портфолио. Форма для <wbr/>вызова замерщика.<br/></div></div></div></div>'
tree_text = fromstring(text, features="html.parser")

result = etree.tostring(tree_text, method="xml", encoding="UTF-8").decode()
logger.debug(result)

result = "\n".join(etree.XPath("//text()")(tree_text))
logger.debug(result)
