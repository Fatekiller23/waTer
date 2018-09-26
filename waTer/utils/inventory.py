# -*- coding: utf-8 -*-
def to_data_points(start_date, stop_date, period):
    """
    由于火币的api只提供最新的2000个data point。。。。那就这样吧。。。

    :param start_date: yyyy-mm-dd
    :param stop_date:  yyyy-mm-dd
    :param period: 1min, 5min, 15min, 30min, 60min, 

     暂时不提供： 1day, 1mon, 1week, 1year
    :return: list
    """
    tables = {'1min': 60, '5min': (5 * 60), '15min': 30 * 60,
              '60min': 60 * 60, '1day': 24 * 60 * 60}

    start = pendulum.from_format(start_date, 'YYYY-MM-DD')
    stop = pendulum.from_format(stop_date, 'YYYY-MM-DD')
    seconds = ((stop.add(days=1) - start)).total_seconds()
    point_numbers = int(seconds / tables[period])

    if point_numbers < 0:
        raise Exception('time is not right!')
    elif point_numbers > 2000:
        log.info('the maixmun data point is 2000.')
        point_numbers = 2000

    return point_numbers