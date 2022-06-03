from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd 
import numpy as np
import os
import pygsheets

from ta.momentum  import RSIIndicator  
from ta.trend import SMAIndicator
import warnings
warnings.filterwarnings("ignore")

import datetime as dt
import time 

def get_metrics(api, max_drawdown):
	acc_details = api.get_account()
	cash_balance = acc_details.cash
	portfolio_value = acc_details.portfolio_value
	acc_status = acc_details.status
	long_market_value = acc_details.long_market_value

	output = pd.DataFrame({
				'cash_balance': [cash_balance],
				'portfolio_value': [portfolio_value],
				'long_market_value': [long_market_value],
				'last_updated':  [dt.datetime.today().strftime('%Y-%m-%d %H:%M')],
				'max_drawdown': [max_drawdown]
				})

	return output