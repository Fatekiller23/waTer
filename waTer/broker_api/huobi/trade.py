# -*- coding: utf-8 -*-
"""
火币行情与交易api的封装模块。提供两个类，一个提供交易功能，一个提供行情功能。
由于websocket不稳定，统一采用rest api。
"""
import base64
import datetime
import hashlib
import hmac
import urllib
import urllib.parse
import urllib.request
from copy import copy
import json
import requests

# global constants
LANGUAGE = 'zh-cn'

DEFAULT_GET_HEADERS = {
    "Content-type": "application/x-www-form-urlencoded",
    'Accept': 'application/json',
    'Accept-Language': LANGUAGE,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

DEFAULT_POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': LANGUAGE,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature


class Market:
    """
    行情api的封装
    """
    MARKET_URL = "https://api.huobi.pro"

    def __init__(self, accessKey='', secreteKey=''):
        self.accessKey = ''
        self.secretKey = ''

    # noinspection PyNoneFunctionAssignment
    def get_k_line(self, symbol, period, size=150):
        """
        获取k线数据
        :param symbol: btcusdt, bchbtc, rcneth 
        规则： 基础币种+计价币种。如BTC/USDT，symbol为btcusdt；ETH/BTC， symbol为ethbtc。以此类推
        
        :param period: 1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
        :param size: [1,2000] 如果数据点超过2000个怎么办？ 这里超过范围直接不返回了。
        :return: list k-line data points.
        """

        params = {'symbol': symbol,
                  'period': period,
                  'size': size}
        url = Market.MARKET_URL + '/market/history/kline'

        res = self.get_request(url, params)

        if res['status'] == 'ok':
            return res['data']
        else:
            print('something wrong in url.')
            return False

    def get_merge_with_symbol(self, symbol):
        """
        获取一个symbol的聚合数据
        
        :param symbol: btcusdt, bchbtc, rcneth 
        :return: 
        
        "tick": {
            "id": K线id,
            "amount": 成交量,
            "count": 成交笔数,
            "open": 开盘价,
            "close": 收盘价,当K线为最晚的一根时，是最新成交价
            "low": 最低价,
            "high": 最高价,
            "vol": 成交额, 即 sum(每一笔成交价 * 该笔的成交量)
            "bid": [买1价,买1量],
            "ask": [卖1价,卖1量]}
        """
        params = {'symbol': symbol}
        url = Market.MARKET_URL + '/market/detail/merged'
        res = self.get_request(url, params)
        if res['status'] == 'ok':
            return res['tick']
        else:
            print('something wrong in url.')
            return False

    def get_merge_with_all(self):
        """
                {  
            "open":0.044297,      // 日K线 开盘价
            "close":0.042178,     // 日K线 收盘价
            "low":0.040110,       // 日K线 最低价
            "high":0.045255,      // 日K线 最高价
            "amount":12880.8510,  // 24小时成交量
            "count":12838,        // 24小时成交笔数
            "vol":563.0388715740, // 24小时成交额
            "symbol":"ethbtc"     // 交易对
        },
        {  
            "open":0.008545,
            "close":0.008656,
            "low":0.008088,
            "high":0.009388,
            "amount":88056.1860,
            "count":16077,
            "vol":771.7975953754,
            "symbol":"ltcbtc"
        }
        :return: 
        """
        url = Market.MARKET_URL + '/market/tickers'
        res = self.get_request(url)
        if res['status'] == 'ok':
            return res['data']
        else:
            print('something wrong in url.')
            return False

    def get_market_depth_with_symbol(self, symbol, dtype):
        """

        :param symbol: btcusdt, bchbtc, rcneth ...
        :param dtype:  step0, step1, step2, step3, step4, step5（合并深度0-5）；step0时，不合并深度
        :return: 
        """
        url = Market.MARKET_URL + '/market/depth'

        params = {'symbol': symbol, 'type': dtype}

        res = self.get_request(url, params)
        if res['status'] == 'ok':
            return res['tick']
        else:
            print('something wrong in url.')
            return False
        pass

    def get_currencys_list(self, ):
        url = Market.MARKET_URL + '/v1/common/currencys'
        res = self.get_request(url)
        if res['status'] == 'ok':
            return res['data']
        else:
            print('something wrong in url.')
            return False
        pass

    def get_accounts(self):
        path = '/v1/account/accounts'
        params = {}
        res = self.key_get_request(path, params)
        if res['status'] == 'ok':
            return res['data']
        else:
            print('something wrong in url.')
            return False

    def get_account_blance(self, account_id):
        path = '/v1/account/accounts/{}/balance'.format(account_id)
        params = {}
        res = self.key_get_request(path, params)
        if res['status'] == 'ok':
            return res['data']
        else:
            print('something wrong in url.')
            return False

    def key_get_request(self, path, params):

        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

        headers = copy(DEFAULT_GET_HEADERS)

        params.update(self.generateSignParams())

        host_url = Market.MARKET_URL
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()

        params['Signature'] = createSign(params, method, host_name, path, self.secretKey)
        url = host_url + path
        if params is not None:
            encoded_params = urllib.parse.urlencode(params)
        else:
            encoded_params = None

        try:
            response = requests.get(url, encoded_params, headers=headers, timeout=5)
            return response.json()
        except BaseException as e:
            print("httpGet failed, detail is:%s" % e)
            return False

    def get_request(self, url, params=None):
        headers = copy(DEFAULT_GET_HEADERS)
        if params is not None:
            encoded_params = urllib.parse.urlencode(params)
        else:
            encoded_params = None

        try:
            response = requests.get(url, encoded_params, headers=headers, timeout=5)
            return response.json()
        except BaseException as e:
            print("httpGet failed, detail is:%s" % e)
            return False

    def generateSignParams(self):
        """生成签名参数"""
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        d = {
            'AccessKeyId': self.accessKey,
            'SignatureMethod': 'HmacSHA256',
            'SignatureVersion': '2',
            'Timestamp': timestamp
        }

        return d



class Trade:
    """
    交易api的封装
    """
    TRADE_URL = "https://api.huobi.pro"

    def __init__(self):
        self.accessKey = 'd13f6000-488c18c2-fb4dbea2-c9c4c'
        self.secretKey = 'b0f5f71e-62a87673-7184b66a-e47e6'

    # 查询某个订单
    def order_info(self, order_id):
        """

        :param order_id: 
        :return: 
        """
        params = {}
        url = "/v1/order/orders/{0}".format(order_id)
        return self.api_key_get(params, url)

    # 查询某个订单的成交明细
    def order_matchresults(self, order_id):
        """

        :param order_id: 
        :return: 
        """
        params = {}
        url = "/v1/order/orders/{0}/matchresults".format(order_id)
        return self.api_key_get(params, url)


    def send_order(self, account_id, amount, source, symbol, _type, price=0):
        """
        :param account_id: 用户账户id
        :param amount: 
        :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
        :param symbol: 
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price: 
        :return: 
        """

        params = {"account-id": account_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": source}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return self.api_key_post(params, url)

    def api_key_post(self, params, request_path):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.accessKey,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = Trade.TRADE_URL
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, self.secretKey)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return self.http_post_request(url, params)

    def api_key_get(self, params, request_path):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.accessKey,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_url = Trade.TRADE_URL
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = createSign(params, method, host_name, request_path, self.secretKey)

        url = host_url + request_path
        return self.http_get_request(url, params)



    def http_post_request(self, url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = json.dumps(params)
        response = requests.post(url, postdata, headers=headers, timeout=10)
        try:

            if response.status_code == 200:
                return response.json()
            else:
                return None
        except BaseException as e:
            print("httpPost failed, detail is:%s,%s" % (response.text, e))
            return None

    def http_get_request(self, url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }
        if add_to_headers:
            headers.update(add_to_headers)

        postdata = urllib.parse.urlencode(params)
        response = requests.get(url, postdata, headers=headers, timeout=5)

        try:

            if response.status_code == 200:
                return response.json()
            else:
                return
        except BaseException as e:
            print("httpGet failed, detail is:%s,%s" % (response.text, e))
            return


if __name__ == '__main__':
    market = Market()
    # data = market.get_k_line(symbol='btcusdt', period='1day', size=200)
    # data = market.get_merge_with_symbol(symbol='btcusdt')
    # data = market.get_merge_with_all()
    # data = market.get_currencys_list()
    # data = market.get_market_depth_with_symbol('ethusdt', 'step0')
    # data = market.get_accounts()
    # data = market.get_account_blance('874796')
    broker = Trade()
    # some = broker.send_order('874796',1,'api','paiusdt','buy-market')
    # data = broker.order_info('10892801359')
    data = broker.order_matchresults('10892801359')
    # print(data)
    pass
