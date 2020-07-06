import os
import requests

from flask import Flask

from dewu.blueprints.api.du_api_blueprint import du_api_bp
from dewu.setting import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_blueprints(app)

    return app


# def register_request(app):
#
#     @app.before_request
#     def set_request_header():
#         headers = {
#             'Host': "app.poizon.com",
#             'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
#                           " Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI "
#                           "MiniProgramEnv/Windows WindowsWechat",
#             'appid': "wxapp",
#             'appversion': "4.4.0",
#             'content-type': "application/json",
#             'Accept-Encoding': "gzip, deflate, br",
#             'Accept': "*/*",
#         }
#         requests.post(headers=headers)
#         requests.get(headers=headers)
#         return requests


def register_blueprints(app):
    app.register_blueprint(du_api_bp, url_prefix='/api')

