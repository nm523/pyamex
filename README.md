# pyamex : American Express account data from Python

![Maintenance](https://img.shields.io/maintenance/no/2019)

## Warning

It looks like Amex have updated their APIs and so this library (and the original ruby libraries) will no longer work.
At present I'm not maintaining this library so unfortunately I won't be providing any updates here.

## Background

Ported from the the ruby version by timrogers, and improvements by DanToml:

* https://github.com/timrogers/amex
* https://github.com/DanToml/amex

Requires Python 3.4 and above.

## Installation

You can install using pip:

```bash
pip install pyamex
```

or manually:

```bash
python setup.py install
```

## Usage

```python

from pyamex import AmexClient
client = AmexClient(username='bill', password='gates', locale='en_GB')

accounts = client.accounts()

# Print all account balances
for account in accounts:
    print(account.card_product, account.total_balance)
```
