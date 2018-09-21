# -*- coding: utf-8 -*-
import time

from waTer.base.dog import BaseDog


class PortfolioDog(BaseDog):
    def __init__(self, listen_queue, reply_queue):
        super().__init__()
        self.listen_queue = listen_queue
        self.reply_queue = reply_queue
        pass

    def run(self,):
            print('portfolio')
            time.sleep(1)
