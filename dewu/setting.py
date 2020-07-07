import logging
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'DDAJDJFQIOWEOWQOQOPTPOFDSJJGJQJJJFJASDJFQIUJAFDAD')
SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


class BaseConfig(object):
    # 添加mysql数据库的配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:{}@{}:3306/dewu?charset=utf8"\
        .format(MYSQL_PASSWORD, SERVER_ADDRESS)
    # 动态追踪设置 追踪对象的修改并返回信号 会额外占用内存
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 设置是否在每次连接结束后自动提交数据库中的变动。
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 打印sql语句 生产环境关闭
    SQLALCHEMY_ECHO = True
    # 添加redis数据库的配置信息
    REDIS_URL = "redis://:{}@{}:6379/0".format(REDIS_PASSWORD, SERVER_ADDRESS)
    # REDIS_URL = "redis://localhost:6379/0"  本地环境redis_url
    SECRET_KEY = SECRET_KEY


class DevelopmentConfig(BaseConfig):
    """调试模式下的app"""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(BaseConfig):
    """生产模式下的app"""
    DEBUG = False
    LOG_LEVEL = logging.ERROR


class TestingConfig(BaseConfig):
    """测试环境下的app"""
    TESTING = True
    WTF_CSRF_ENABLED = False


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    'testing': TestingConfig
}
