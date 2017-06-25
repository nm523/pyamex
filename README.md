# pyamex
## Access American Express account data from Python

Based on the work by timrogers, and improvements by DanToml:

* https://github.com/timrogers/amex
* https://github.com/DanToml/amex

Requires Python 3.5+ above

## TODO
* Code cleanup
* Improved installer
* Documentation
* Examples

## Usage

```

from pyamex import AmexClient
client = AmexClient(username='bill', password='gates', locale='en_GB')

# Print all account balances
for account in client.accounts():
    print(account.card_product, account.total_balance)

```

## License

MIT
