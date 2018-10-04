# -*- coding: utf-8 -*-

import tushare as ts

pro = ts.pro_api()
df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='daily',
                 start_date='20180701', end_date='20180801')
