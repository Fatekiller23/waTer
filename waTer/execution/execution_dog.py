# -*- coding: utf-8 -*-
import time
from logbook import Logger
from waTer.base.dog import BaseDog
from waTer.base.event import FillEvent
log = Logger('execution')

class ExecuteDog(BaseDog):
    def __init__(self, listen_queue, reply_queue):
        super().__init__()
        self.listen_queue = listen_queue
        self.reply_queue = reply_queue
        pass

    def run(self):
        log.debug('hi')
        while True:
            order_event = self.listen_queue.get()
            log.debug("get order event!")

            log.debug("request to broker")
            log.debug("make response to fill event")

            fill_evt = FillEvent()
            self.reply_queue.put(fill_evt)
            time.sleep(1)
