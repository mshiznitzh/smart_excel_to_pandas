import hashlib
import logging

#Setup Logging for Module
logger = logging.getLogger(__name__)

def md5(fname):
    logger.info('Started Function')
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()