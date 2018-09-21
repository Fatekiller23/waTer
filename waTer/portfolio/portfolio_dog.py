# -*- coding: utf-8 -*-
import time
from logbook import Logger
from waTer.base.dog import BaseDog
from waTer.base.event import OrderEvent
log = Logger('portfolio')

class PortfolioDog(BaseDog):
    def __init__(self, listen_queue, reply_queue):
        super().__init__()
        self.listen_queue = listen_queue
        self.reply_queue = reply_queue
        pass

    def run(self):
        log.debug('hi')
        while True:
            event = self.listen_queue.get()

            if event.simple_type == 'S':
                log.debug("get signal event!")
                order_evt = OrderEvent()
                log.debug("put order event")
                self.reply_queue.put(order_evt)

            elif event.simple_type == 'F':
                log.debug("get Fill event!")
                log.debug("good trade, 已经更新了")
            time.sleep(1)

