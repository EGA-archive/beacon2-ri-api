import pymongo
from beacon import conf

client = pymongo.MongoClient("mongodb://{}:{}@{}:{}/{}?authSource={}".format(
    conf.database_user,
    conf.database_password,
    conf.database_url,
    conf.database_port,
    conf.database_name,
    conf.database_auth_source
))
