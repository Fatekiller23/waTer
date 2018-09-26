# -*- coding: utf-8 -*-
from brain.brain import Brain
from logbook import Logger

from waTer.utils.read_conf import get_conf
from waTer.utils.setup_logger import setup_logger

log = Logger('running')


def start_app():
    conf = get_conf('configuration/app_conf.toml')
    log_conf = conf['log']
    setup_logger(log_conf)
    return conf


if __name__ == '__main__':
    conf = start_app()
    brain = Brain(conf)
    brain.go()
