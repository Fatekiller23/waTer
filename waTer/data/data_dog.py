# -*- coding: utf-8 -*-

import time

from waTer.base.dog import BaseDog


class DataDog(BaseDog):
    def __init__(self, listen_queue, reply_queue):
        super().__init__()
        self.listen_queue = listen_queue
        self.reply_queue = reply_queue

    def run(self,):

        while True:
            print('data!')
            time.sleep(1)
