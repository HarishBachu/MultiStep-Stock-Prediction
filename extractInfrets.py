import numpy as np 
import pandas as pd 

from libraries.ewt_transform import EWT1D
from libraries.helpers import findInfrets, getLowFreqComponent 

import os
from tqdm import tqdm, trange 

import yfinance as yf
import argparse 

def getWindows(data, windowSize):
    windows = []
    for i in trange(len(data)//windowSize, desc="Making Windows"):
        window = data[i*windowSize : (i+1)*windowSize] 
        windows.append(window)
    return windows 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--scrip", type=str, required=True)
    parser.add_argument("--start", type=str, required=True)
    parser.add_argument("--end", type=str, required=True)
    parser.add_argument("--window", type=int, required=True)
    parser.add_argument("--smooth", type=bool, required=False, default=True)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--decomp", type=int, required=False, default=6)
    parser.add_argument("--n", type=int, required=False, default=5) 

    args = parser.parse_args() 

    data = yf.download(args.scrip, args.start, args.end)    
    close = list(data["Close"])

    if args.window > len(close):
        args.window = len(close)

    windows = getWindows(close, args.window) 

    rets = np.array(
        [findInfrets(
            window, n=args.n, smooth=args.smooth, order=args.order, decomp=args.decomp
        ) for window in windows]
    ) 

    stockWindows = {
        "window" : windows, 
        "rets": rets,
        "dates": list(data.index)
    }

    if args.smooth:
        output = open("smoothedRets_{}.pkl".format(args.scrip), "wb")
        pickle.dump(stockWindows, output)
        output.close()
        # np.save("smoothedRets_{}.npy".format(args.scrip), rets)
    else:
        output = open("rets_{}.pkl".format(args.scrip), "wb")
        pickle.dump(stockWindows, output)
        output.close()
        # np.save("Rets_{}.npy".format(args.scrip), rets)


