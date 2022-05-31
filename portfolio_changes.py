from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd 
import numpy as np
import os
from alpaca_trade_api import REST
import pygsheets
import datetime as dt

def get_trading_cal(api):
    cal = api.get_calendar()
    cal_ls = []
    for c in cal:
        cal_ls.append(c.date)
      
    cal_ls = pd.Series(cal_ls)
    return cal_ls

def get_portfolio_changes(api):
    acc_start = api.get_account().created_at.strftime('%Y-%m-%d') # the date where account was created

    cal_ls = get_trading_cal(api) # obtain trading calendar

    # Obtain the trading days that were between the account created date and today, then convert to date format
    trading_days = cal_ls[(cal_ls >= acc_start) & (cal_ls < dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d'))]
    trading_days = trading_days.apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))

    # Obtain the portfolio changes
    df_trade = pd.DataFrame(columns = ['timestamp','equity','pnl','pnl (pct)'])

    for trade in trading_days:
        result = api.get_portfolio_history(trade)
        profit_loss = result.profit_loss
        pnl_pct = result.profit_loss_pct
        timestamp = [dt.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M') for val in result.timestamp]
        df_trade = pd.concat([df_trade, pd.DataFrame({'timestamp': timestamp, 'equity': result.equity, 'pnl':profit_loss, 'pnl (pct)': pnl_pct })], axis = 0)

    # Remove duplicates record with the same date
    df_trade = df_trade.sort_values(by = 'timestamp').drop_duplicates(subset = ['timestamp'],ignore_index=True, keep = 'first')

    df_trade['date'] = df_trade['timestamp'].apply(lambda x: x[:10])

    # Only query the last record of the day for intraday changes
    df_agg = df_trade.groupby('date').last()
    df_agg = df_agg.reset_index().drop('timestamp', axis = 1)

    df_agg['max_drawdown'] = 10000 - df_agg.equity.min()
    
    return df_agg