
import mplfinance as mpf
import yfinance as yf
import datetime as DT


msft = yf.Ticker("MSFT")
history = msft.history(period="max")
today = DT.datetime.now().strftime("%Y-%m-%d")
previous = (DT.datetime.now() - DT.timedelta(days=7)).strftime("%Y-%m-%d")
ohlc = history.loc[previous: today,]


ohlc.index.name = 'Date'
ohlc.shape
ohlc.head(3)
ohlc.tail(3)
mpf.plot(ohlc,type='candle')
