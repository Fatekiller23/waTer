# -*- coding: utf-8 -*-

import pendulum
import pandas
import pandas as pd
import numpy as np

start = lambda eqd: eqd.index[0]

end = lambda eqd: eqd.index[-1]

average = lambda eqd: eqd[eqd != 0].mean()

average_gain = lambda eqd: eqd[eqd > 0].mean()

average_loss = lambda eqd: eqd[eqd < 0].mean()

win_rate = lambda eqd: float(sum(eqd > 0)) / len(eqd)

payoff = lambda eqd: eqd[eqd > 0].mean() / -eqd[eqd < 0].mean()

pf = PF = lambda eqd: abs(eqd[eqd > 0].sum() / eqd[eqd < 0].sum())

# 暂时没想明白。。。
maxdd = lambda eqd: (eqd.cumsum().expanding().max() - eqd.cumsum()).max()

rf = RF = lambda eqd: eqd.sum() / maxdd(eqd)

_days = lambda eqd: eqd.resample('D').sum().dropna()


def sharpe(eqd):
    ''' daily sharpe ratio '''
    d = _days(eqd)
    return (d.mean() / d.std()) * (252 ** 0.5)


# 索提诺比率
def sortino(eqd):
    ''' daily sortino ratio '''
    d = _days(eqd)
    return (d.mean() / d[d < 0].std()) * (252 ** 0.5)


# 溃败指数，衡量下跌中的波动性
def ulcer(eqd):
    eq = eqd.cumsum()
    return (((eq - eq.expanding().max()) ** 2).sum() / len(eq)) ** 0.5


# upi交易指数
def upi(eqd, risk_free=0):
    eq = eqd[eqd != 0]
    return (eq.mean() - risk_free) / ulcer(eq)


UPI = upi


# 魔改的upi
def mpi(eqd):
    """ Modified UPI, with enumerator resampled to months (to be able to
    compare short- to medium-term strategies with different trade frequencies. """
    return eqd.resample('M').sum().mean() / ulcer(eqd)


MPI = mpi


# 可能是最大回撤随机排列
def mcmdd(eqd, runs=100, quantile=0.99, array=False):
    maxdds = [maxdd(eqd.take(np.random.permutation(len(eqd)))) for i in range(runs)]
    if not array:
        return pd.Series(maxdds).quantile(quantile)
    else:
        return maxdds


# ----------------------------------------------------------------------------- 以上为指标

def days(eqd):
    first = pendulum.from_format(str(eqd.index[0]), 'YYYY-MM-DD')
    last = pendulum.from_format(str(eqd.index[-1]), 'YYYY-MM-DD')
    res = (last - first).days
    return res


def _format_out(v, precision=4):
    """
    这个函数式 按不同格式，进行标准化输出，老外还是牛逼呀。
    :param v: 
    :param precision: 
    :return: 
    """
    if isinstance(v, dict):
        return {k: _format_out(v) for k, v in list(v.items())}
    if isinstance(v, (float, np.float)):
        v = round(v, precision)
    if isinstance(v, np.generic):
        return np.asscalar(v)
    return v


def performance_summary(equity_diffs, quantile=0.99, precision=4):
    eqd = equity_diffs[equity_diffs != 0]
    eqd.index = pandas.DatetimeIndex(eqd.index)

    if len(eqd) == 0:
        # 在此过程中没有产生交易
        return {}

    # backtest summary
    backtest = {
        'from': start(eqd),
        'to': end(eqd),
        'days': days(eqd),
        'trades': len(eqd),
    }

    # performance summary

    performance = {
        'profit': eqd.sum(),
        'averages': {
            'trade': average(eqd),
            'gain': average_gain(eqd),
            'loss': average_loss(eqd),
        },
        'winrate': win_rate(eqd),
        'payoff': payoff(eqd),
        'PF': PF(eqd),
        'RF': RF(eqd),
    }

    risk_return_profile = {
        'sharpe': sharpe(eqd),
        'sortino': sortino(eqd),
        'maxdd': maxdd(eqd),
        'WCDD (monte-carlo {} quantile)'.format(quantile): mcmdd(eqd, quantile=quantile),
        'UPI': UPI(eqd),
        'MPI': MPI(eqd),
    }

    res = {
        'backtest': backtest,
        'performance': performance,
        'risk/return profile': risk_return_profile,
    }

    return _format_out(res)
