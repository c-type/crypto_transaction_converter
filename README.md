# Bitcoin.de Transaction Conversion Tool

Simple tool to convert the transaction csv table provided by the crypto market place [bitcoin.de](https://www.bitcoin.de/en) into a more standard format such as used by TurboTax and on [CoinTracker](https://www.cointracker.io/).
The conversion tool greatly simplifies dealing with US taxes for [bitcoin.de](https://www.bitcoin.de/en) users.

# Usage

1. Navigate to the git repository
2. `./bc_csv_converter.py --in_file ./data/sample_bitcoin_de_transactions.csv`
3. This will write a converted table called `output.csv` into the current directory. Alternatively, an additional option `--out_file <output_file.csv>` can be provided to control the output table filename and location.

# Limitations

- Focused on transactions between BTC and EUR
- Handles: Sales, Purchases, and Disbursements

# Donation 

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=KDDKU6QJHQLL6)
