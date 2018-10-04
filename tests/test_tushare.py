# -*- coding: utf-8 -*-
import tushare as ts
ts.set_token('')
pro = ts.pro_api()

df = pro.trade_cal(exchange_id='SSE', start_date='20180101', end_date='', fields='pretrade_date', is_open='0')
