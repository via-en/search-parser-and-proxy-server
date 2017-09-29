import os,sys
import logging.config
from mongo_structures.utils import init_connection
from mongo_structures.models import Post

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_DIR, 'logging.conf'))
logger = logging.getLogger(__name__)

connection_url = "{}/{}".format("mongodb://79.135.230.130:20707","YandexData")
init_connection(connection_url)
uniq_id = "e83c6bfd9a975b149e68e8b2fd896b8b"
result = Post.objects(ID=uniq_id).count()

result = Post.objects(ID=uniq_id).update_one(add_to_set__CrawlId=1,add_to_set__HashTags=1)
logger.debug(result)
for post in Post.objects(ID=uniq_id):
    logger.debug(post.ID)
