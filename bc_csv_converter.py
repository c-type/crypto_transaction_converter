import pandas as pd
import pathlib
import datetime
import numpy as np 

PARENT_DIR = pathlib.Path(__file__).resolve().parent

in_file_path = PARENT_DIR / 'testdata/sample_bitcoin_de_transactionsc.csv'
out_file_path = PARENT_DIR / 'testdata/cointracker_table.csv'

bc_df = pd.read_csv(in_file_path, sep=';')

def format_cols(df: pd.DataFrame)->pd.DataFrame:
    """Format assign right data types to columns"""
    df_formatted = df.copy()
    
    bitcoin_fmt = '%Y-%m-%d %H:%M:%S'
    date_series = [datetime.datetime.strptime(date_str, bitcoin_fmt) for date_str in df_formatted.iloc[:,0]]

    df_formatted.iloc[:,0] = date_series
    return df_formatted
#    for i, string in enumerate(df_formatted[:,0]):
      
bc_df = format_cols(bc_df)
cointracker_cols = ['Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency', 'Tag']

ct_df = pd.DataFrame(columns=cointracker_cols)

cointracker_format = '%m/%d/%Y %H:%M:%S'
date_series = [dt.strftime(cointracker_format) for dt in bc_df.iloc[:,0]]

# Handle Dates
ct_df['Date'] = date_series

# Handle Purchases
purch_idx = np.where(bc_df['Type'] == 'Purchase')[0]
ct_df['Received Quantity'][purch_idx] = bc_df['BTC incl. fee'][purch_idx]
ct_df['Received Currency'][purch_idx] = 'BTC'
ct_df['Sent Quantity'][purch_idx] = bc_df['amount before fee'][purch_idx]
ct_df['Sent Currency'][purch_idx] = 'EUR'
ct_df['Fee Amount'][purch_idx] = bc_df['BTC incl. fee'][purch_idx] - bc_df['BTC excl. Bitcoin.de fee'][purch_idx]
ct_df['Fee Currency'][purch_idx] = 'BTC'

# Handle Sales
sale_idx = np.where(bc_df['Type'] == 'Sale')[0]
ct_df['Received Quantity'][sale_idx] = bc_df['amount before fee'][sale_idx]
ct_df['Received Currency'][sale_idx] = 'EUR'
ct_df['Sent Quantity'][sale_idx] = bc_df['BTC incl. fee'][sale_idx]
ct_df['Sent Currency'][sale_idx] = 'BTC'
ct_df['Fee Amount'][sale_idx] = bc_df['amount before fee'][sale_idx] - bc_df['amount after Bitcoin.de-fee'][sale_idx]
ct_df['Fee Currency'][sale_idx] = 'EUR'

# Handle Disbursement
disburse_idx = np.where(bc_df['Type'] == 'Disbursement')[0]
ct_df['Fee Amount'][disburse_idx] = np.abs(bc_df['Incoming / Outgoing'][disburse_idx+1])
ct_df['Fee Currency'][disburse_idx] = 'BTC'
ct_df['Sent Quantity'][disburse_idx] = np.abs(bc_df['Incoming / Outgoing'][disburse_idx])
ct_df['Sent Currency'][disburse_idx] = 'BTC'
ct_df['Tag'][disburse_idx] = 'gift'

# Drop NAN lines
ct_df.drop(index=np.where(ct_df['Fee Currency'].isna())[0], inplace=True)

# Write CSV table
ct_df.to_csv(out_file_path, index=False)
