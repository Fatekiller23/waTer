# -*- coding: utf-8 -*-
import pandas


def signals_to_positions(signals, init_pos=0):
    pos = init_pos  # pos 是每日持仓量，就按一手来。

    # ps 是最后要返回的
    ps = pandas.Series(0., index=signals.index)

    for time, sig in signals.iterrows():

        if pos != 0:
            if sig['buy']:
                pos += sig['buy']  # 这里想方便一些
            if sig['sell']:
                pos -= 1
        if pos == 0:
            if sig['buy']:
                pos += sig['buy']  # 这里想方便一些
            if sig['sell']:
                pass
        ps[time] = pos
    # return ps[ps != ps.shift()] #
    return ps  # 这里考虑好去除重叠的仓位有必要么？


def extract_frame(info_obj):
    df = dict()
    df['buy'] = info_obj.get('buy')
    df['sell'] = info_obj.get('sell')

    return pandas.DataFrame(df)


def trades_to_equity(trade_matrix):
    def _cmp_fn(x):
        """
        :param x: 
        :return: 
        """
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

    # 定义方向
    position_signal = trade_matrix.position.apply(_cmp_fn)

    # 前一个元素与后一个元素有变化的位置
    close_point = position_signal != position_signal.shift()

    # 形容不出来，就是可以算
    equity = (trade_matrix.vol * trade_matrix.price).cumsum()[close_point] - \
             (trade_matrix.position * trade_matrix.price)[close_point]

    # 一笔交易后的静值 +的赚了， -的赔了
    equity = equity.diff()

    equity = equity.reindex(trade_matrix.index).fillna(value=0)

    equity[equity != 0] *= -1  # 将方向扳正

    return equity


class Slicer(object):
    def __init__(self, target, obj):
        self.target = target
        self.__len__ = obj.__len__

    def __getitem__(self, x):
        return self.target(x)
