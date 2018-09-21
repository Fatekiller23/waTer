# -*- coding: utf-8 -*-
import time
from logbook import Logger
from waTer.base.dog import BaseDog
log = Logger('strategy')

class StrategyDog(BaseDog):
    def __init__(self, listen_queue, reply_queue):
        super().__init__()
        self.listen_queue = listen_queue
        self.reply_queue = reply_queue
        pass

    def run(self):
        log.debug('hi')
        while True:

            time.sleep(1)
