import numpy as np
from numpy.lib.arraysetops import isin 
from libraries.ewt_transform import EWT1D
import sys


def findTrend(window):
    '''
    Purpose: Check whether a signal is in an uptrend or not
    
    Inputs: 
    window  ->  list/np.ndarray

    Outputs: 
    trend direction ->  bool
    '''
    d_window = [window[i+1] - window[i] for i in range(len(window)-1)]
    return sum(d_window) >= 0 


def bestTrend(prices):
    '''
    Purpose: Tells us what is the best place (index) to buy and sell. 
    In other words, it tells us what is the maximum difference possible between 2 points.
    (Smaller value appears first)
    
    Inputs: 
    prices  ->  prices window(list)

    Outputs: 
    tuple   ->  (
        buyIdx  ->  best buy location(int), 
        sellIdx ->  best sell location(int), 
        profit  ->  max profit possible(float)
    ) 
    '''
    # print(prices)
    minSoFar = sys.maxsize 
    profit = 0
    maxProfit = 0
    buyIdx = 0
    sellIdx = 0 
    for i in range(len(prices)):
        minSoFar = min(minSoFar, prices[i])
        if minSoFar == prices[i]:
            buyIdx = i 
        profit = prices[i] - minSoFar 
        maxProfit = max(maxProfit, profit)
        if maxProfit == profit:
            sellIdx = i
    return (buyIdx, sellIdx, profit)


def findFibrets(window, n=5, smooth=True, order=2, decomp=6):
    '''
    Purpose: Given a local window, it tries to approximate the fibonacci retracements (Fibrets)
    Finds trend of local window, followed by points for best uptrend or downtrend. 
    Based on these start and end locations, and trend, the Fibrets are calculated 

    Inputs: 
    window  -> prices window(list), 
    n       -> number of retracements(int)

    Outputs:
    rets    -> fibonacci retracements(list)
    tuple   ->  (
        s   ->  start of best trend(int), 
        e   ->  end of best trend(int)
    )
    '''
    upTrend = findTrend(window)
    percs = [0.236, 0.382, 0.5, 0.618, 0.786]
    rets = []
    if smooth == True:
        window = getLowFreqComponent(window, order, decomp)
    # print(upTrend)
    # print(window)
    if upTrend:
        s, e, _ = bestTrend(window)
        end = window[e]
        start = window[s]
        delta = end - start 
        for p in percs:
            rets.append(end - (delta*p))
    else:
        s, e, _ = bestTrend(window[::-1])
        s = len(window) - s - 1
        e = len(window) - e - 1  
        start = window[s]
        end = window[e]
        delta = start - end
        for p in percs:
            rets.append(end + (delta*p))
    return rets, (s, e)


#Add Comment for this 
def getLowFreqComponent(window, order, n=6):
    window = np.asarray(window)
    # print(window)
    ewt = EWT1D(window, n)[0].T
    lowFreq = np.zeros_like(window)
    for o in range(order):
        lowFreq += ewt[o]
    # print(lowFreq)
    return lowFreq  
    