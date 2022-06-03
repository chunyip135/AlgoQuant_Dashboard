from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd 
import numpy as np
import os
from alpaca_trade_api import REST
import pygsheets

def get_all_transactions(api):
    result = api.get_activities()

    result_df = pd.DataFrame()

    #print(result[0]) # cum_qty, price, symbol, transaction_time

    result_df = pd.DataFrame(columns = ['Qty','price','symbol','transaction_time'])

    qty_list = []
    price_list = []
    symbol_list = []
    transaction_time_list = []
    type_list = []

    for res in result:
        qty_list.append(res.cum_qty)
        price_list.append(res.price)
        symbol_list.append(res.symbol)
        transaction_time_list.append(res.transaction_time)
        type_list.append(res.side)



    result_df = pd.DataFrame({
        'Qty': qty_list, 
        'Price': price_list, 
        'Symbol': symbol_list, 
        'Transaction_time': transaction_time_list, 
        'Type': type_list})

    return result_df

def realized_profit_df(api):

    result_df = get_all_transactions(api)

    df_buy = result_df[result_df.Type == 'buy']

    df_sell = result_df[result_df.Type == 'sell']

    df = pd.merge(df_buy, df_sell, on = 'Symbol', how = 'right', suffixes = ['_buy','_sell'])

    #print(df_sell)

    testing = df_sell.sort_values(by = 'Transaction_time')

    testing['Price'] = testing.Price.astype('float')
    df_buy['Price'] = df_buy.Price.astype('float')

    output_frame = pd.DataFrame(columns = ['Symbol', 'Qty','Avg_cost','Avg_holding_period',
                                 'Earliest_buy_time','Latest_buy_time','Sell_time','Profit_per_unit','Total Profit', 'Winning_bet?'])

    for sym in testing.Symbol.unique():
        #print(sym)
        buy = df_buy.loc[df_buy.Symbol == sym]
        sell = testing.loc[testing.Symbol == sym]

        obs = [] # completed sell\'s index
        for i, row in sell.iterrows():
            output_dic = {}
            if i not in obs:
                out = buy.loc[(buy.Transaction_time < row.Transaction_time)]
                idx = [j for j in out.index if j not in obs]
                out = out.loc[idx]
                assert out.shape[0] == int(row.Qty)
                
                # Avg_cost
                #print(row.Price - out.groupby('Symbol').Price.mean())
                #print(row.Transaction_time - out.groupby('Symbol').Transaction_time.mean())
                output_dict = {'Symbol': sym, 
                               'Qty': int(row.Qty), 
                               'Avg_cost': round(out.groupby('Symbol').Price.mean()[0],2),
                               'Avg_holding_period': (row.Transaction_time - out.groupby('Symbol').Transaction_time.mean())[0],
                               'Earliest_buy_time': out.groupby('Symbol').Transaction_time.min()[0],
                               'Latest_buy_time': out.groupby('Symbol').Transaction_time.max()[0],
                               'Sell_time': row.Transaction_time,
                               'Profit_per_unit': round(row.Price - out.groupby('Symbol').Price.mean()[0],2),
                               'Total Profit': round((row.Price - out.groupby('Symbol').Price.mean())[0] * int(row.Qty),2),
                               'Winning_bet?': True if round(row.Price - out.groupby('Symbol').Price.mean()[0],2) > 0 else False}
                output_frame = output_frame.append(output_dict, ignore_index = True)
                
                if len(idx) > 1:
                    for ix in idx:
                        obs.append(ix)
                else:
                    obs.append(idx[0])
            

    output_frame = output_frame.sort_values('Sell_time', ascending = False)
    output_frame['Avg_holding_period'] = output_frame['Avg_holding_period'].apply(lambda x: x.days)

    return output_frame