#!/usr/bin/env python

import pandas as pd
import pathlib
import datetime
import numpy as np 
import click

@click.command()
@click.option('--in_file', default='./data/sample_bitcoin_de_transactions.csv', 
        help='The path to the input csv file obtained from bitcoin.de')
@click.option('--out_file', default='./data/output.csv', 
        help='Output path for the converted csv file. If just the filename '
        'is provided, saves into the directory where this script lives.')
def convert(in_file: str, out_file: str)->None:
    """Main conversion function"""
    
    # Setup file paths
    PARENT_DIR = pathlib.Path(__file__).resolve().parent
    in_file = PARENT_DIR / in_file
    out_file = PARENT_DIR / out_file

    # Read in bitcoin.de csv file
    bc_df = pd.read_csv(in_file, sep=';')

    # Initialize output dataframe
    cointracker_cols = ['Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency', 'Tag']
    ct_df = pd.DataFrame(columns=cointracker_cols)

    # Handle Transactions
    ct_df = format_dates(bc_df, ct_df)
    ct_df = handle_purchases(bc_df, ct_df)
    ct_df = handle_sale(bc_df, ct_df)
    ct_df = handle_disbursements(bc_df, ct_df)

    # Drop NAN lines
    ct_df.drop(index=np.where(ct_df['Fee Currency'].isna())[0], inplace=True)
    # Write CSV table
    ct_df.to_csv(out_file, index=False)
    
    print(f'Table successfully converted and written to {out_file}')


def format_dates(bc_df: pd.DataFrame, ct_df:pd.DataFrame)->pd.DataFrame:
    """Format assign right data types to columns"""
    bitcoin_fmt = '%Y-%m-%d %H:%M:%S'
    date_series = [datetime.datetime.strptime(date_str, bitcoin_fmt) for date_str in bc_df.iloc[:,0]]
    cointracker_format = '%m/%d/%Y %H:%M:%S'
    ct_df['Date'] = [dt.strftime(cointracker_format) for dt in date_series]
    return ct_df

def handle_purchases(bc_df, ct_df):
    """Handle Purchases"""
    purch_idx = np.where(bc_df['Type'] == 'Purchase')[0]
    ct_df['Received Quantity'][purch_idx] = bc_df['BTC incl. fee'][purch_idx]
    ct_df['Received Currency'][purch_idx] = 'BTC'
    ct_df['Sent Quantity'][purch_idx] = bc_df['amount before fee'][purch_idx]
    ct_df['Sent Currency'][purch_idx] = 'EUR'
    ct_df['Fee Amount'][purch_idx] = bc_df['BTC incl. fee'][purch_idx] - bc_df['BTC excl. Bitcoin.de fee'][purch_idx]
    ct_df['Fee Currency'][purch_idx] = 'BTC'
    return ct_df

def handle_sale(bc_df, ct_df):
    """Handle Sales"""
    sale_idx = np.where(bc_df['Type'] == 'Sale')[0]
    ct_df['Received Quantity'][sale_idx] = bc_df['amount before fee'][sale_idx]
    ct_df['Received Currency'][sale_idx] = 'EUR'
    ct_df['Sent Quantity'][sale_idx] = bc_df['BTC incl. fee'][sale_idx]
    ct_df['Sent Currency'][sale_idx] = 'BTC'
    ct_df['Fee Amount'][sale_idx] = bc_df['amount before fee'][sale_idx] - bc_df['amount after Bitcoin.de-fee'][sale_idx]
    ct_df['Fee Currency'][sale_idx] = 'EUR'
    return ct_df

def handle_disbursements(bc_df, ct_df):
    """Handle Disbursement"""
    disburse_idx = np.where(bc_df['Type'] == 'Disbursement')[0]
    ct_df['Fee Amount'][disburse_idx] = np.abs(bc_df['Incoming / Outgoing'][disburse_idx+1])
    ct_df['Fee Currency'][disburse_idx] = 'BTC'
    ct_df['Sent Quantity'][disburse_idx] = np.abs(bc_df['Incoming / Outgoing'][disburse_idx])
    ct_df['Sent Currency'][disburse_idx] = 'BTC'
    ct_df['Tag'][disburse_idx] = 'gift'
    return ct_df


if __name__ == '__main__':
    convert()
