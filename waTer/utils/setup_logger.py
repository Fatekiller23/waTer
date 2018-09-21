# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""A modoule wrapper to logbook
This module can let you define easy log configration with
five variables.
    ·debug          boolean
    ·logfile        path
    ·backup_count   int
    ·max_size       bytes
    ·format_string  string
    ·level          int
for more infomation, check out this official site:
    http://logbook.readthedocs.io/en/stable/index.html
"""
import os
import sys

from logbook import StreamHandler, RotatingFileHandler
from logbook import set_datetime_format

# show local time in log line timestamp
set_datetime_format('local')


def setup_logger(conf):
    """ setup logger for app
    take conf, and set it.
    :param conf: a dict of logbook conf.
    """
    level_dict = {'notset': 9, 'debug': 10, 'info': 11, 'warning': 12, 'error': 13, 'critical': 14}
    debug = conf['debug']
    logfile = conf['logfile']
    backup_count = conf['backup_count']
    max_size = conf['max_size']
    format_string = conf['format_string']
    level = level_dict[conf['level']]

    if debug:
        StreamHandler(sys.stdout, format_string=format_string, level=level).push_application()
    else:

        full_log_path = os.path.abspath(logfile)
        dir_path = os.path.dirname(full_log_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        RotatingFileHandler(logfile, mode='a', encoding='utf-8',
                            level=level, format_string=format_string, delay=False,
                            max_size=max_size, backup_count=backup_count,
                            filter=None, bubble=True).push_application()
