# -*- coding: utf-8 -*-
"""
数据载入模块
"""

import pandas as pd
import tushare as ts

# 拟使用 tushare 的api
ts.set_token('')
pro = ts.pro_api()


def load_from_tushare(ticker='000001.SZ', start='20180701', stop='20180801'):
    """ 
    使用tushare 的api 获取股票日线数据
    
    
    1. pd.panel 2.for t in ticker dictionary 
    """

    if isinstance(ticker, list):
        return pd.Panel(
            {t: load_from_tushare(
                ticker=t, start=start, stop=stop)
                for t in ticker})

    data = to_format(pro.daily(ts_code=ticker, start_date=start, stop=stop))
    ohlc_cols = ['open', 'high', 'low', 'close', 'volume']
    data = data.rename(columns={'open': 'O', 'high': 'H', 'low': 'L',
                                'close': 'C',
                                'vol': 'V'})
    return data


def to_format(data):
    data = data.loc[:, ['open', 'high', 'low', 'close', 'vol', 'trade_date']]
    date = data.trade_date.apply(date_change)
    data.insert(0, 'Date', date)
    data = data.set_index('Date')
    data.index = pd.DatetimeIndex(data.index)
    data.pop('trade_date')
    return data.sort_index()


def date_change(date):
    return '-'.join([date[0:4], date[4:6], date[6:]])
