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

from gsheets import update_gsheets
from metrics import get_metrics
import hydra
from omegaconf import DictConfig
from hydra.utils import to_absolute_path as abspath

@hydra.main(config_path='../config', config_name = 'main')
def process_credentials(config: DictConfig):
    cronitor.api_key = config.cronitor.api_key

    os.environ['APCA_API_KEY_ID'] = config.alpaca.api_key_id
    os.environ['APCA_API_SECRET_KEY'] = config.alpaca.api_secret_key
    os.environ['APCA_API_BASE_URL'] = config.alpaca.api_base_url

    os.environ['SERVICE_FILE'] = config.gsheets.path
    os.environ['GSHEETS_KEY'] = config.gsheets.key

    return None

@cronitor.job('dashboard-job')
def main():

    api = REST()

    print('Extracting data ...')
    print('Transforming data ...')
    result_df = get_all_transactions(api)
    realized_profit_output = realized_profit_df(api)
    unrealized_profit_output = full_df_pipeline(api)
    portfolio_changes_output, max_drawdown = get_portfolio_changes(api)
    metrics_output = get_metrics(api, max_drawdown)

    try:
        print('Updating Google Sheets ...')
        update_gsheets(service_file = os.environ['SERVICE_FILE'], 
            key = os.environ['GSHEETS_KEY'],
            transactions = result_df, 
            realized_profit = realized_profit_output, 
            unrealized_profit = unrealized_profit_output, 
            portfolio_changes = portfolio_changes_output, 
            metrics_values = metrics_output)
        print('Script updated at {}'.format(dt.datetime.today().strftime('%Y-%m-%d %H:%M')))
    except:
        print('Script not updated at {}'.format(dt.datetime.today().strftime('%Y-%m-%d %H:%M')))
    return None

if __name__ == "__main__":
    process_credentials()
    main()
# Obtain unrealized profits
# Obtain open postiion and their details
# pie chart of the stocks holding 
# realized returns
# unrealized returns
# maximum drawdown
