import hashlib
import math
import time
import requests

from flask import Blueprint, jsonify, json, request
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
# 首页数据流 {"sign":"5e22051c5156608a85b12d501d615c61","tabId":"","limit":20,"lastId":1}
index_load_more_url = 'https://app.poizon.com/api/v1/h5/index/fire/index'
# 最近购买接口 {"sign":"f44e26eb08becbd16b7ed268d83b3b8c","spuId":"73803","limit":20,"lastId":"","sourceApp":"app"}
recensales_load_more_url = 'https://app.poizon.com/api/v1/h5/commodity/fire/last-sold-list'
# 商品详情接口 {"sign":"5721d19afd7a7891b627abb9ac385ab0","spuId":"49413","productSourceName":"","propertyValueId":"0"}
product_detail_url = 'https://app.poizon.com/api/v1/h5/index/fire/flow/product/detail'


# 转换签名
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


# 关键词搜索商品
@du_api_bp.route('/search/<string:keywords>', methods=['GET'])
def product_search_by_keyword(keywords):
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


# 商品详情页面
@du_api_bp.route('/product/details', methods=['POST'])
def product_details():
    json_data = request.json
    productSourceName = json_data['productSourceName']
    propertyValueId = json_data['propertyValueId']
    spuId = json_data['spuId']

    post_data = {
        'spuId': spuId,
        'productSourceName': productSourceName,
        'propertyValueId': propertyValueId,
        'sign': return_sign(
            'productSourceName{}propertyValueId{}spuId{}19bc545a393a25177083d4a748807cc0'
            .format(productSourceName, propertyValueId, spuId)
        )
    }

    post_data = str(post_data).encode('utf-8')
    res_data = requests.post(product_detail_url, headers=headers, data=post_data).text
    return jsonify(res_data)


# 最近购买
@du_api_bp.route('/recent/purchase', methods=['POST'])
def recent_purchase_list():
    json_data = request.json
    lastId = json_data['lastId']
    spuId = json_data['spuId']

    post_data = {
        'limit': 20,
        'spuId': spuId,
        'lastId': lastId,
        'sourceApp': 'app',
        'sign': return_sign('lastId{}limit20sourceAppappspuId{}19bc545a393a25177083d4a748807cc0'.format(lastId, spuId))
    }

    post_data = str(post_data).encode('utf-8')
    res_data = requests.post(recensales_load_more_url, headers=headers, data=post_data).text
    return jsonify(res_data)


# 首页数据流
@du_api_bp.route('/index/list', methods=['POST'])
def index_load_data():
    json_data = request.json
    lastId = json_data['lastId']

    post_data = {
        'tabId': '',
        'limit': 20,
        'lastId': lastId,
        'sign': return_sign('lastId{}limit20tabId19bc545a393a25177083d4a748807cc0'.format(lastId)),
    }

    post_data = str(post_data).encode('utf-8')
    res_data = requests.post(index_load_more_url, headers=headers, data=post_data).text
    return jsonify(res_data)


# 品牌列表页商品接口
@du_api_bp.route('/index/list', methods=['POST'])
def brand_list():
    json_data = request.json
    page = json_data['page']
    sortType = json_data['sortType']
    sortMode = json_data['sortMode']
    catId = json_data['catId']
    unionId = json_data['unionId']
    title = json_data['title']

    sign = return_sign(
        'catId{}limit20page{}showHot-1sortMode{}sortType{}title{}unionId{}19bc545a393a25177083d4a748807cc0'
        .format(catId, page, sortMode, sortType, title, unionId)
    )

    print(sign)
    url = 'https://app.poizon.com/api/v1/h5/search/fire/search/list?' \
          'sign={}&title={}&page={}&sortType={}' \
          '&sortMode={}&limit=20&showHot=-1&catId={}&unionId={}'.format(
                sign, title, page, sortType, sortMode, catId, unionId
          )

    res_data = requests.get(url, headers=headers).text
    return jsonify(res_data)
