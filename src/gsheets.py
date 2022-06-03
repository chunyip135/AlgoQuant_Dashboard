import pandas as pd
import numpy as np
import os
from alpaca_trade_api import REST
import pygsheets
from realized_profit import realized_profit_df, get_all_transactions
from unrealized_profits import full_df_pipeline
from portfolio_changes import get_portfolio_changes
import datetime as dt
import cronitor

def connect_client(service_file):
	try:
		client = pygsheets.authorize(service_file=service_file)
		return client
	except:
		print('Google sheets is not authorized successfully.')	

def update_gsheets(service_file, key, 
	transactions, realized_profit, 
	unrealized_profit, portfolio_changes, metrics_values):
	client = connect_client(service_file)
	sh = client.open_by_key(key)

	try:
	    wk1 = sh[0] # open first worksheet of spreadsheet or sh.sheet1

	    wk1.clear()

	    wk1.set_dataframe(realized_profit, 'A1')
	    print('Realized profit\'s Table is updated.')
	    # wk1.update_value('I{}'.format(output_frame.shape[0] + 2), output_frame['Total Profit'].sum())
	except:
		print('Realized profit\'s Table is not updated.')

	try:
	    wk2 = sh[1]

	    wk2.clear()

	    wk2.set_dataframe(unrealized_profit, 'A1')
	    print('Unrealized profit\'s Table is updated.')
	except:
		print('Unrealized profit\'s Table is not updated.')
    
	try:
	    wk3 = sh[2]

	    wk3.clear()

	    wk3.set_dataframe(portfolio_changes, 'A1')
	    print('Portfolio changes\' Table is updated.')
	except:
		print('Portfolio changes\' Table is not updated.')

	try:
	    wk4 = sh[3]

	    wk4.clear()
	    wk4.set_dataframe(transactions, 'A1')
	    print('Transactions\' Table is updated.')
	except:
		print('Transactions\' Table is not updated.')

	try:
		wk5 = sh[4]

		wk5.set_dataframe(metrics_values, 'A1')
		print('Metrics\' Table is updated')
	except:
		print('Metrics\' Table is not updated')

	return None

