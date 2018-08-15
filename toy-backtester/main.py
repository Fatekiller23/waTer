# Declare the components with respective parameters
from data import HistoricCSVDataHandler
from strategy import BuyAndHoldStrategy
from portfolio import NaivePortfolio
from execution import SimulatedExecutionHandler
import queue
from queue import  Queue
import time













if __name__ == '__main__':

    events = Queue()

    bars = HistoricCSVDataHandler(events,csv_dir='', symbol_list=['000001'])
    strategy = BuyAndHoldStrategy(bars, events)
    port = NaivePortfolio(bars=bars, events=events, start_date='2018-05-01')
    broker = SimulatedExecutionHandler(events)


    while True:
        # Update the bars (specific backtest code, as opposed to live trading)
        if bars.continue_backtest:
            bars.update_bars()
        else:
            break
        # Handle the events
        while True:
            try:
                event = events.get(False)
            except queue.Empty:
                break
            else:
                if event is not None:
                    if event.type == 'MARKET':
                        print("market event")
                        strategy.calculate_signals(event)
                        port.update_timeindex(event)

                    elif event.type == 'SIGNAL':
                        print("signal event")
                        port.update_signal(event)

                    elif event.type == 'ORDER':
                        print("order event")
                        broker.execute_order(event)

                    elif event.type == 'FILL':
                        print("fill event")
                        port.update_fill(event)
                        # port.create_equity_curve_dataframe()
                        # port.output_summary_stats()

        # 10-Minute heartbeat
        time.sleep(10)