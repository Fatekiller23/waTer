# -*- coding: utf-8 -*-
import time

class countdown:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False


    def run(self, n):
        while (n > 0):
            if self._running:
                print("T-minus", n)
                n -= 1
                time.sleep(1)
            else:
                break


from threading import Thread

# t = Thread(target=countdown, args=(5,))
# t.start()
# t.join()

if __name__ == '__main__':
    # t = Thread(target=countdown, args=(5,))
    c = countdown()
    t = Thread(target=c.run, args=(5,),)
    t.start()
    c.terminate()

    # 书上说 daemonic 的线程不能join，然而这里是可以的。不join直接终结，join会等待。
    t.join()  # join 的用法就是召唤之后锁住这个线程，不让他的任何方法调用。
    # print(t.is_alive())
