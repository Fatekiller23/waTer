# -*- coding: utf-8 -*-

import time

from logbook import Logger

from waTer.base.dog import BaseDog
from waTer.base.event import MarketEvent

log = Logger('data')


class DataDog(BaseDog):
    def __init__(self, listen_queue, reply_queue):
        super().__init__()
        self.listen_queue = listen_queue
        self.reply_queue = reply_queue

    def run(self):
        log.debug('hi')

        while True:
            event = MarketEvent()
            self.reply_queue.put(event)
            time.sleep(1)
