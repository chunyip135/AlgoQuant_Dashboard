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

def get_open_positions(api):
	open_positions = api.list_positions()

	asset_class_ls = []
	avg_entry_price_ls = []
	change_today_ls = []
	cost_basis_ls = []
	current_price_ls = []
	exchange_ls = []
	lastday_price_ls = []
	market_value_ls = []
	qty_ls = []
	side_ls = []
	symbol_ls = []
	unrealized_intraday_pl_ls = []
	unrealized_intraday_plpc_ls = []
	unrealized_pl_ls = []
	unrealized_plpc_ls = []

	for pos in open_positions:
	    asset_class_ls.append(pos.asset_class)
	    avg_entry_price_ls.append(pos.avg_entry_price)
	    change_today_ls.append(pos.change_today)
	    cost_basis_ls.append(pos.cost_basis)
	    current_price_ls.append(pos.current_price)
	    exchange_ls.append(pos.exchange)
	    lastday_price_ls.append(pos.lastday_price)
	    market_value_ls.append(pos.market_value)
	    qty_ls.append(pos.qty)
	    side_ls.append(pos.side)
	    symbol_ls.append(pos.symbol)
	    unrealized_intraday_pl_ls.append(pos.unrealized_intraday_pl)
	    unrealized_intraday_plpc_ls.append(pos.unrealized_intraday_plpc)
	    unrealized_pl_ls.append(pos.unrealized_pl)
	    unrealized_plpc_ls.append(pos.unrealized_plpc)
	    
	op_df = pd.DataFrame({'Symbol': symbol_ls, 
	                      'Asset_class': asset_class_ls, 
	                      'Qty': qty_ls,
	                      'Avg_entry_price': avg_entry_price_ls,
	                      'Change_today': change_today_ls,
	                      'Cost_basis': cost_basis_ls, 
	                      'Current_price': current_price_ls,
	                      'Exchange': exchange_ls,
	                      'Lastday_price': lastday_price_ls,
	                      'Market_value': market_value_ls,
	                      'Side': side_ls,
	                      'Unrealized_intraday_pl ($)': unrealized_intraday_pl_ls,
	                      'Unrealized_intraday_pl (%)': unrealized_intraday_plpc_ls,
	                      'Unrealized_pl ($)': unrealized_pl_ls,
	                      'Unrealized_pl (%)': unrealized_plpc_ls
	                     })

	# Convert the columns format
	op_df['Avg_entry_price'] = op_df['Avg_entry_price'].astype('float')
	op_df['Change_today'] = op_df['Change_today'].astype('float')
	op_df['Current_price'] = op_df['Current_price'].astype('float')
	op_df['Lastday_price'] = op_df['Lastday_price'].astype('float')
	op_df['Market_value'] = op_df['Market_value'].astype('float')
	op_df['Unrealized_intraday_pl ($)'] = op_df['Unrealized_intraday_pl ($)'].astype('float')
	op_df['Unrealized_intraday_pl (%)'] = op_df['Unrealized_intraday_pl (%)'].astype('float')
	op_df['Unrealized_pl ($)'] = op_df['Unrealized_pl ($)'].astype('float')
	op_df['Unrealized_pl (%)'] = op_df['Unrealized_pl (%)'].astype('float')
	op_df['Qty'] = op_df['Qty'].astype('int')

	op_df['Avg_entry_price'] = op_df.Avg_entry_price.round(2)

	op_df = op_df.sort_values(by = 'Unrealized_pl (%)', ascending = False)
	op_df['Unrealized_pl (%)'] = op_df['Unrealized_pl (%)'].mul(100)
	op_df['Unrealized_intraday_pl (%)'] = op_df['Unrealized_intraday_pl (%)'].mul(100)

	return op_df


def get_trading_cal(api):
    cal = api.get_calendar()
    cal_ls = []
    for c in cal:
        cal_ls.append(c.date)
      
    cal_ls = pd.Series(cal_ls)
    return cal_ls

def get_data(api, stock_ls, start, end = None):
    
  # first_half
    indexes = np.arange(0,len(stock_ls),5)
    for i in range(len(indexes)-1):
        data = api.get_bars(
                      symbol =  stock_ls[indexes[i]:indexes[i+1]],
                      timeframe = TimeFrame.Day,
                      start = start,
                      end = end,
                      limit = 10000,
                      adjustment= 'raw',
                      ).df
        if i == 0:
            db = data
        else:
            db = db.append(data)
    return db

def RSI_SMA(data, symbol_list):
    alerts = []
    for symbol in symbol_list:
        df = data.loc[data.symbol == symbol] # get individual stock price


        # Calculate technical indicators
        rsi4 = RSIIndicator(df.close, window = 4)

        sma200 = SMAIndicator(df.close, 200)

        df['rsi4'] = rsi4.rsi()
        df['sma200'] = sma200.sma_indicator()
        
        try:
            latest = df.iloc[-1,:] # obtain latest indicators' values
        except:
            alerts.append([symbol,None, None])

        alerts.append([symbol,latest.rsi4, latest.sma200])

    alerts_df = pd.DataFrame(alerts, columns=['Symbol','RSI4','SMA200'])
    alerts_df.set_index('Symbol', inplace = True)

    return alerts_df

def full_df_pipeline(api):

	op_df = get_open_positions(api)

	cal_ls = get_trading_cal(api)
	tdy_date = dt.datetime.strftime(dt.datetime.today(), format = '%Y-%m-%d')
	last_trading_date = pd.Timestamp(cal_ls[cal_ls[cal_ls <= tdy_date].index[-3]]).strftime('%Y-%m-%d')
	print(last_trading_date)

	df_data = get_data(api, op_df.Symbol.unique(), start = '2019-01-01', end = last_trading_date)

	df_ta = RSI_SMA(df_data,op_df.Symbol.unique())

	full_df = op_df.join(df_ta, on = 'Symbol')
	full_df = full_df.set_index(np.arange(full_df.shape[0]))

	return full_df



# maximum drawdown?


