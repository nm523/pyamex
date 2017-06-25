# pyamex : American Express account data from Python

Ported from the the ruby version by timrogers, and improvements by DanToml:

* https://github.com/timrogers/amex
* https://github.com/DanToml/amex

Requires Python 3.4 and above.

## Installation

For the moment, you'll have to clone or download this directory.
Once inside the directory (with the setup.py file) run:

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

## Examples
See below.

## TODO
* Code cleanup
* Examples


