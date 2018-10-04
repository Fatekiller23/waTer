# -*- coding: utf-8 -*-
import pandas as pd
import pendulum
from cached_property import cached_property

import water_v.parts
import water_v.performance


class BackTest:
    """
    回测主体（向量化回测）
    
    接受交易信号与交易价格，组成账户曲线。
    """

    _ohlc_possible_name = 'ohlc', 'ohlcv', 'kdata'

    def __init__(self, info_object, name='test'):
        self.name = name

        # 获取全局变量，并将所有key都变成小写。
        self._info_dict = dict([(k.lower(), v) for k, v in info_object.items()])

        self.running_time = pendulum.now().to_datetime_string()

        pass

    def __repr__(self):
        return "Backtest: {}, running time:{}".format(self.name, self.running_time)

    @property
    def info_dict(self):
        return self._info_dict

    @cached_property
    def ohlc(self):
        for possible_name in self._ohlc_possible_name:
            ohlc = self._info_dict.get(possible_name)
            if ohlc is not None:
                return ohlc
        raise Exception("ohlc data is not found in info_object")

    @cached_property
    def signals(self):
        """
        获取info_dict里面的交易信号序列
        
        # 如果信号序列里有空的，就填False 相当于不动。
        :return:  
        """

        return water_v.parts.extract_frame(self.info_dict).fillna(value=False)

    @cached_property
    def positions(self):
        return water_v.parts.signals_to_positions(self.signals)

    @cached_property
    def trades(self):
        # 构造一个trade 矩阵，分为三列
        # 仓位， 价格， 交易手数
        some = {
            'position': self.positions,
            'price': self.trade_price,
            'vol': self.positions.diff()
        }
        return pd.DataFrame(some).dropna()

    @cached_property
    def prices(self):

        # 暂时使用 default_price，以后改成用户自定义的序列
        return self.default_price

    @cached_property
    def trade_price(self):
        pr = self.prices
        if pr is None:
            return self.ohlc.O  # .shift(-1)
        return pr

    @cached_property
    def default_price(self):
        return self.ohlc.O

    @cached_property
    def equity(self):
        """
        这里把交易变成股本
        :return: 
        """
        return water_v.parts.trades_to_equity(self.trades)

    @cached_property
    def report(self):
        return water_v.performance.performance_summary(self.equity)

    def plot_equity(self, subset=None, ax=None):
        """
        同样是个画图函数，画出账户的钱数

        :param subset: 
        :param ax: 
        :return: 
        """
        import matplotlib.pylab as pylab
        _ = None  # 这句应该没什么卵用
        if ax is None:
            _, ax = pylab.subplots()  # 画子图

        if subset is None:
            subset = slice(None, None)
        assert isinstance(subset, slice)  # 调用slice的子图

        # eq = self.equity[subset].cumsum()  # cumsum 是什么鬼

        eq = self.equity.iloc[subset].cumsum()

        eq.plot(color='red', label='strategy', ax=ax)
        ix = self.ohlc[str(eq.index[0]):str(eq.index[-1])].index
        price = self.ohlc.C

        # 一个series - 一个scalar
        (price[ix] - price[ix][0]).resample('W').first().dropna() \
            .plot(color='black', alpha=0.5, label='underlying', ax=ax)

        ax.legend(loc='best')
        ax.set_title(str(self))
        ax.set_ylabel('Equity for %s' % subset)
        return _, ax

    def plot_trades(self, subset=None, ax=None):
        """
        this is a digram function.


        :param subset: 
        :param ax: 
        :return: 
        """
        if subset is None:
            # what ???
            subset = slice(None, None)

        # using self trades, get trade result
        fr = self.trades.iloc[subset]

        le = fr.price[(fr.position > 0) & (fr.vol > 0)]
        # se = fr.price[(fr.position < 0) & (fr.vol < 0)]
        lx = fr.price[(fr.position.shift() > 0) & (fr.vol < 0)]
        # sx = fr.price[(fr.position.shift() < 0) & (fr.vol > 0)]

        import matplotlib.pylab as pylab
        _ = None
        if ax is None:
            # ax for handle
            _, ax = pylab.subplots()

        ax.plot(le.index, le.values, '^', color='lime', markersize=12,
                label='long enter')

        ax.plot(lx.index, lx.values, 'o', color='red', markersize=7,
                label='long exit')
        # ax.plot(le.values, '^', color='lime', markersize=12,
        #         label='long enter')
        #
        # ax.plot(lx.values, 'o', color='lime', markersize=7,
        #         label='long exit')

        # ax.plot(se.index, se.values, 'v', color='red', markersize=12,
        #         label='short enter')

        # ax.plot(sx.index, sx.values, 'o', color='red', markersize=7,
        #         label='short exit')

        self.ohlc.O.iloc[subset].plot(color='black', label='price', ax=ax)
        ax.set_ylabel('Trades for %s' % subset)
        return _, ax
