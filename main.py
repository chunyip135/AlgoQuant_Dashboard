#!/Users/samuelwong/opt/anaconda3/envs/algo_trade/bin/python
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

cronitor.api_key = '45b0013337744758895bf85013e1dc8d'

os.environ['APCA_API_KEY_ID'] = 'PKCHDD6J9DQDE7BZZ1UV'
os.environ['APCA_API_SECRET_KEY'] = 'lQ5hWAXPrGx2F0jEO0eiDULu1w2cOiG2liCeX101'
os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'

@cronitor.job('important-background-job')
def main():
    api = REST()

    result_df = get_all_transactions(api)
    realized_profit_output = realized_profit_df(api)
    unrealized_profit_output = full_df_pipeline(api)
    portfolio_changes_output = get_portfolio_changes(api)

    client = pygsheets.authorize(service_file='algoquant-351309-ae021cd7392e.json')

    sh = client.open_by_key('1hPxsuwdDvpZpQYG2yi_djwcDG1RDAw1RcS-QZ5prUPo')

    wk1 = sh[0] # open first worksheet of spreadsheet or sh.sheet1

    wk1.clear()

    wk1.set_dataframe(realized_profit_output, 'A1')
    # wk1.update_value('I{}'.format(output_frame.shape[0] + 2), output_frame['Total Profit'].sum())

    wk2 = sh[1]

    wk2.clear()

    wk2.set_dataframe(unrealized_profit_output, 'A1')

    wk3 = sh[2]

    wk3.clear()

    wk3.set_dataframe(portfolio_changes_output, 'A1')

    wk4 = sh[3]

    wk4.clear()
    wk4.set_dataframe(result_df, 'A1')

    print('Script updated at {}'.format(dt.datetime.today().strftime('%Y-%m-%d %H:%M')))
    return None

main()
# Obtain unrealized profits
# Obtain open postiion and their details
# pie chart of the stocks holding 
# realized returns
# unrealized returns
# maximum drawdown
