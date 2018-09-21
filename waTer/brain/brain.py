# -*- coding: utf-8 -*-
import time
from queue import Queue
from threading import Thread, Event

from waTer.broker_api.backtest.broker_dog import BrokerDog
from waTer.data.data_dog import DataDog
from waTer.execution.execution_dog import ExecuteDog
from waTer.portfolio.portfolio_dog import PortfolioDog
from waTer.strategy.strategy_dog import StrategyDog
from logbook import Logger

log = Logger('brain')

class Brain:
    """
    这个类加载所有需要线程，并完成一次通知工作。
    """

    def __init__(self):
        # listen barks(event) from dog. ^^
        self.listen_channel = Queue()

        # tell commands(event) to dog.  ^^
        self.queue_set = [Queue(), Queue(), Queue(), Queue(), Queue()]

        self.to_data_dog = self.queue_set[0]
        self.to_strategy_dog = self.queue_set[1]
        self.to_portfolio_dog = self.queue_set[2]
        self.to_execution_dog = self.queue_set[3]
        self.to_broker_dog = self.queue_set[4]

        pass

    def load(self):
        """
        加载所有线程，完成队列架设
        :return: 
        """

        # init dogs
        broker_dog = BrokerDog(self.to_broker_dog, self.listen_channel)
        data_dog = DataDog(self.to_data_dog, self.listen_channel)
        execute_dog = ExecuteDog(self.to_execution_dog, self.listen_channel)
        portfolio_dog = PortfolioDog(self.to_portfolio_dog, self.listen_channel)
        strategy_dog = StrategyDog(self.to_strategy_dog, self.listen_channel)

        # name instances
        broker_dog.name = 'broker'
        data_dog.name = 'data'
        execute_dog.name = 'execute'
        portfolio_dog.name = 'portfolio'
        strategy_dog.name = 'strategy'

        # init work threads set
        workers = [data_dog, strategy_dog, portfolio_dog, execute_dog, broker_dog]

        # start,stop event
        self.start_evt = start_evt = Event()

        # start workers instance
        i = 0
        for worker in workers:
            thread = Thread(target=worker.run,
                            name='%s' % worker.name,
                            daemon=True)
            thread.start()
            i += 1

    def go(self):
        """
        运行整个动作
        :return: 
        """
        # 加载启动相应工作线程
        self.load()

        # coordinate events from listen queue.

        while True:
            if not self.listen_channel.empty():
                # get event
                event = self.listen_channel.get()

                # discern event type
                who_s = self.who_s_meat(event)

                # to corresponding dog
                who_s.put(event)

            else:
                log.debug('no event, wating!')
                time.sleep(1)

    def who_s_meat(self, event):

        type_dict = {
            'B': self.to_broker_dog,
            'O': self.to_execution_dog,
            'S': self.to_portfolio_dog,
            'F': self.to_portfolio_dog,
            'M': self.to_strategy_dog,
            'D': self.to_data_dog}

        return type_dict[event.simple_type]

    def give_a_test(self):
        """
        发送一个test指令，每个线程回复一条消息
        所有线程都完好，就是正常的。
        :return: 
        """
        raise NotImplementedError
