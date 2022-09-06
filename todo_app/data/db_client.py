from distutils.command.config import config
import pymongo


class Client(object):
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, config):
        if cls._instance is None:
            cls._instance = pymongo.MongoClient(config.DB_CONNECTION_STRING)
        return cls._instance
