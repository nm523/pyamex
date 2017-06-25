import datetime
import pyamex.utils
import urllib.parse
import urllib.request
import xml.etree.cElementTree
from collections import defaultdict
from .transaction import Transaction

class CardAccount:

    loyalty_programmes = []

    def __init__(self, options):
        # options is a dict containing the
        # XML properties pulled directly from the API
        # xml
        for key, value in options.items():
            setattr(self, pyamex.utils.clean_key(key), value)

    def transactions(self, billing_period=0, 
                     transaction_type='pending'):

        result = defaultdict(list)
        billing_periods = pyamex.utils.to_list(billing_period)

        for period in billing_periods:
            options = { 
                'PayLoadText' : self.client.transactions_request_xml(
                                                       card_index=self.card_index, 
                                                       billing_period=period, 
                                                       transaction_type=transaction_type)
                }
            options = urllib.parse.urlencode(options) \
                                  .encode()

            response = urllib.request.urlopen(self.client.url, options) \
                                     .read()

            xml_tree = xml.etree.cElementTree.fromstring(response)

            for transaction in xml_tree.findall('StatementDetails/CardAccounts/CardAccount/TransactionDetails/Transaction'):
                result[period].append(Transaction(transaction))

        return result

    def is_credit_card(self):
        return self.lending_type == 'Credit'

    def is_charge_card(self):
        return self.lending_type == 'Charge'

    def get_payment_due_date(self):
        if self.payment_due_date:
            return datetime.datetime.strptime(self.payment_due_date, '%d %b %Y')
        return ''

    def overdue(self):
        return True if self.past_due else False

    def due(self):
        return float(self.payment_due) > 0

    def card_type(self):
        if self.is_basic:
            return 'basic'
        elif self.is_platinum:
            return 'platinum'
        elif self.is_centurion:
            return 'centurion'
        elif self.is_premium:
            return 'premium'
        else:
            return 'unknown'

    def loyalty_enabled(self):
        return self.loyalty_indicator

    def loyalty_balances(self):
        return { programme.name : programme.balance
                 for programme in self.loyalty_programmes.items() }

