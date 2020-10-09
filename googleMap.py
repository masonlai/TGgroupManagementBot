#!/usr/bin/env python
# -*- coding: utf-8 -*-
# utf-8 --> 可以打中文
import yfinance as yf
msft = yf.Ticker("MSFT")
print(msft.history(period="7"))

# simple argument 旺角/日式
def map(area,type):
    url = ''
    return url