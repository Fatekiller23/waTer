# -*- coding: utf-8 -*-

import time

from logbook import Logger

from waTer.base.dog import BaseDog
from waTer.base.event import MarketEvent
from .data_models import WaterData

log = Logger('data')


def set_ts(token):
    import tushare as ts
    ts.set_token(token)
    pro = ts.pro_api()
    return pro


def to_water_data_structure(data_frame):
    """
    接收到从api 返回来的数据
    :param raw_data: 
    :return: 
    """
    return WaterData(data_frame)


class DataDog(BaseDog):
    """
    负责任务：
        数据的载入{存储，该怎么存呢，参考quantaxis}
        易用的数据操作结构（pandas 和 numpy 已经很易用，那么在其上面包一层，应该会更加好）
        自己生成Market Event，促使数据一个个喂给strategy。
        
    """

    def __init__(self, listen_queue, reply_queue, conf):
        super().__init__()
        self.listen_queue = listen_queue
        self.reply_queue = reply_queue
        self.token = conf['token']

        # set ts
        self.data_source = set_ts(self.token)

    def run(self):
        log.debug('hi')

        data = self.get_k_data('btcusdt', 'daily', '2018-05-23', '2018-09-25')
        while True:
            # 当有数据时
            bar, status = data.update_bar()
            if status == 0:
                event = MarketEvent(bar)
                self.reply_queue.put(event)
            # 当数据循环完了时
            else:
                log.debug('数据迭代完毕')
                break
            time.sleep(1)  # for debugging use.

    def get_k_data(self, symbol, freq, start_date, end_date):
        """
        symbol 可以直接用 
        period 也可以用
        start_date 和 stop_date 需要按period 化成多大的size
        
        获取行情数据
        
        :param symbol: 
        :param freq: 
        :param start_date: 
        :param stop_date: 
        :return: 
        """

        data_frame = self.data_source.coinbar(exchange='huobi', symbol=symbol,
                                              freq=freq, start_date=start_date, end_date=end_date)

        water_data = to_water_data_structure(data_frame)

        return water_data


if __name__ == '__main__':
    # test data points
    # number = to_data_points('2018-07-22', '2018-07-23', '1min')

    pass
