import requests
import datetime
import pyamex.utils
import xml.etree.cElementTree
from collections import defaultdict
from .transaction import Transaction


class CardAccount:
    """
    Contains the account details for a given card associated
    with an Amex account.

    Contains methods for obtaining the transactions associated
    with the account, as well as some data about the account itself.

    Attributes
    ----------
    Attributes are generated dynamically from the keys given in the
    options dictionary on initialisation.

        loyalty_programmes (list of pyamex.loyalty.LoyaltyProgramme): The loyalty programmes attached to the card
    """

    loyalty_programmes = []

    def __init__(self, options):
        """
        Parameters
        ----------
        options : dict
            dict of parameters
        """
        for key, value in options.items():
            setattr(self, pyamex.utils.clean_key(key), value)

    def transactions(self, billing_period=0,
                     transaction_type='recent'):
        """
        Gets the most recent transactions for an account, 
        or those within a period specified.

        Parameters
        ----------
        billing_period : int or list of ints (default: 0)
            The billing period to be inspected, if a list of ints
            is passed through, then the transactions for each period
            will be extracted.

        transaction_type : str (default: 'recent')
            Toggles between 'pending' and 'recent' transactions

        Returns : dict of lists
        """
        result = defaultdict(list)
        billing_periods = pyamex.utils.to_list(billing_period)

        for period in billing_periods:
            options = {
                'PayLoadText': self.client.transactions_request_xml(
                    card_index=self.card_index,
                    billing_period=period,
                    transaction_type=transaction_type)
            }

            response = requests.get(self.client.url, options) \
                .content

            xml_tree = xml.etree.cElementTree.fromstring(response)

            status = xml_tree.find('ServiceResponse/Status').text
            if status != 'success':
                raise requests.exceptions.RequestException()

            for transaction in xml_tree.findall(
                    'StatementDetails/CardAccounts/CardAccount/TransactionDetails/Transaction'):
                result[period].append(Transaction(transaction))

        return result

    @property
    def is_credit_card(self):
        return self.lending_type == 'Credit'

    @property
    def is_charge_card(self):
        return self.lending_type == 'Charge'

    def get_payment_due_date(self):
        if self.payment_due_date:
            return datetime.datetime.strptime(self.payment_due_date, '%d %b %Y')
        return ''

    @property
    def overdue(self):
        return True if self.past_due else False

    @property
    def due(self):
        return float(self.payment_due) > 0

    @property
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

    @property
    def loyalty_enabled(self):
        return self.loyalty_indicator

    def get_loyalty_balances(self):
        return {
            programme.name: programme.balance
            for programme in self.loyalty_programmes
        }

    def __repr__(self):
        repr_ = '<pyamex.card.CardAccount ({card})>'
        return repr_.format(card=self.card_product.encode('utf-8'))
