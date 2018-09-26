# -*- coding: utf-8 -*-
class Event:
    """
    Event is base class providing an interface for all subsequent 
    (inherited) events, that will trigger further events in the 
    trading infrastructure.   
    """


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with 
    corresponding bars.
    """

    def __init__(self, bar_data):
        """
        Initialises the MarketEvent.
        """
        self.type = 'MARKET'
        self.simple_type = 'M'
        self.bar_data = bar_data

    def __repr__(self):

        return "MarketEvent"


class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """

    def __init__(self,):
        """
        Initialises the SignalEvent.
        Parameters:
        symbol - The ticker symbol, e.g. 'GOOG'. '10001' 股票名
        datetime - The timestamp at which the signal was generated.
        signal_type - 'LONG' or 'SHORT'.
        """

        self.type = 'SIGNAL'
        self.simple_type = 'S'



class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit)(市价，限价),
    quantity and a direction.
    """

    def __init__(self,):
        """
        Initialises the order type, setting whether it is
        a Market order ('MKT') or Limit order ('LMT'), has
        a quantity (integral) and its direction ('BUY' or
        'SELL').
        Parameters:
        symbol - The instrument to trade.
        order_type - 'MKT' or 'LMT' for Market or Limit.
        quantity - Non-negative integer for quantity.
        direction - 'BUY' or 'SELL' for long or short.
        """

        self.type = 'ORDER'
        self.simple_type = 'O'


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from a brokerage. Stores the quantity of an instrument
    actually filled and at what price. In addition, stores
    the commission of the trade from the brokerage.
    """

    def __init__(self):
        """
        Initialises the FillEvent object. Sets the symbol, exchange,
        quantity, direction, cost of fill and an optional 
        commission.
        If commission is not provided, the Fill object will
        calculate it based on the trade size and Interactive
        Brokers fees.
        Parameters:
        timeindex - The bar-resolution when the order was filled.
        symbol - The instrument which was filled.
        exchange - The exchange where the order was filled. 实盘交易价格
        quantity - The filled quantity.
        direction - The direction of fill ('BUY' or 'SELL')
        fill_cost - The holdings value in dollars.
        commission - An optional commission sent from IB.
        """

        self.type = 'FILL'
        self.simple_type = 'F'


