#!/usr/bin/env python
# -*- coding: utf-8 -*-
# utf-8 --> 可以打中文
import yfinance as yf
import datetime as DT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import pandas
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler

msft = yf.Ticker("MSFT")
history = msft.history(period="max")
today = DT.datetime.now().strftime("%Y-%m-%d")
previous = (DT.datetime.now() - DT.timedelta(days=7)).strftime("%Y-%m-%d")
data = history.loc[previous: today, ['Open', 'Close']]

data.reset_index().plot(x='Date', y=['Open','Close'], kind='line')
plt.show()


# simple argument 旺角/日式
def map(area, type):
    url = ''
    return url
