# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC


class BaseDog(ABC):
    """
    BaseDog是我们勤劳的狗的原型，其他的类别狗都是从这里演化出来的。
    他的后代可以帮我们干很多事情。
    """

    def __init__(self, ):
        self._running = True
        pass

    def terminate(self):
        self._running = False

    def __repr__(self):
        raise NotImplementedError

    def close(self):
        return not self._running

    @abstractmethod
    def run(self,):
        raise NotImplementedError

    def reply_for_good(self):
        self.reply_queue.put("good")
