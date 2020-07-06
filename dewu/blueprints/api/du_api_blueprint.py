import hashlib
import math
import time
import requests

from flask import Blueprint, jsonify, json
from urllib.parse import quote

du_api_bp = Blueprint('du_api_blueprint', __name__)

# 请求头部
headers = {
    'Host': "app.poizon.com",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI "
                  "MiniProgramEnv/Windows WindowsWechat",
    'appid': "wxapp",
    'appversion': "4.4.0",
    'content-type': "application/json",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept': "*/*",
}
# 首页数据流
index_load_more_url = 'https://app.poizon.com/api/v1/h5/index/fire/index'
# 最近购买接口
recensales_load_more_url = 'https://app.poizon.com/api/v1/h5/commodity/fire/last-sold-list'
# 商品详情接口
product_detail_url = 'https://app.poizon.com/api/v1/h5/index/fire/flow/product/detail'


# 获取签名
def return_sign(raw_sign_code_str):
    # md5原始sign的字符串
    m = hashlib.md5()
    m.update(raw_sign_code_str.encode("utf8"))
    sign = m.hexdigest()
    return sign


# 请求搜索接口
def handle_search_api(keywords, page=0):
    sortMode = 1
    sortType = 1

    sign = return_sign(
        'limit20page{}showHot-1sortMode{}sortType{}title{}unionId19bc545a393a25177083d4a748807cc0'
        .format(page, sortMode, sortType, keywords)
    )
    print(sign)

    url = 'https://app.poizon.com/api/v1/h5/search/fire/search/list?' \
          'sign={}&title={}&page={}&sortType={}' \
          '&sortMode={}&limit=20&showHot=-1&unionId='.format(sign, quote(keywords), page, sortType, sortMode)
    res_data = requests.get(url, headers=headers).text
    return json.loads(res_data)['data']


# 关键词搜索商品接口
@du_api_bp.route('/search/<string:keywords>', methods=['GET'])
def goods_search_by_keyword(keywords):
    res_data = handle_search_api(keywords)
    # print(res_data)

    collection = []
    count = math.ceil(int(res_data['total']) / 20)
    for i in range(count):
        productList = handle_search_api(keywords, i)['productList']
        # data = {}
        # for j in productList:
        #     data = {
        #         'productId': productList[j]['productId'],
        #         'title': productList[j]['title'],
        #         'price': productList[j]['price'],
        #         'logoUrl': productList[j]['logoUrl']
        #     }
        collection.extend(productList)
        print('第%d次' % i)
        time.sleep(3)

    return jsonify(collection)
