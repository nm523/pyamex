import os
import uuid
import time
import requests
import requests.exceptions
import pkg_resources
import xml.etree.cElementTree
from .card import CardAccount
from .loyalty import LoyaltyProgramme

# For accessing the XML templates in the data directory
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(FILE_PATH, 'data')


class AmexClient:
    """
    Main entry point for accessing the Amex API.
    """

    all_urls = {
        'en_GB': {
            'base_uri': 'https://global.americanexpress.com',
            'accounts': '/myca/intl/moblclient/emea/ws.do?Face=en_GB'
        },
        'en_US': {
            'base_uri': 'https://online.americanexpress.com',
            'accounts': '/myca/moblclient/us/v2/ws.do'
        },
        'de_DE': {
            'base_uri': 'https://slglobal.americanexpress.com',
            'accounts': '/myca/intl/moblclient/emea/ws.do?Face=de_DE'
        }
    }

    loyalty_programmes = []

    def __init__(self, username, password, locale='en_GB'):
        """
        Parameters
        ----------
        username : str
            Username of the account holder

        password : str
            Password for the user

        locale : str
           Decides which API url to use
        """
        self.locale = locale
        self.username = username
        self.password = password

        urls = self.all_urls[locale]
        self.url = ''.join([urls['base_uri'], urls['accounts']])

    def accounts(self):
        """
        Queries the API for all of the card accounts for the user

        Returns : list of CardAccounts

        """
        # get the summary data
        options = {'PayLoadText': self.request_xml()}

        response = requests.get(self.url, params=options) \
            .content

        xml_tree = xml.etree.cElementTree.fromstring(response)

        status = xml_tree.find('ServiceResponse/Status').text

        if status != 'success':
            raise requests.exceptions.RequestException()

        self.security_token = xml_tree.find('ClientSecurityToken').text

        accounts = [
            self.create_account(account)
            for account in xml_tree.find('CardAccounts')
        ]

        return accounts

    def create_account(self, account_tree):
        """
        Extract data from an xml account tree and return
        a CardAccount object containing all of the relevant fields

        Parameters
        ----------
        account_tree : xml.etree.cElementTree.Element
            An XML tree containing the account data

        Returns : CardAccount

        """

        # Couple this object to the account object in order
        # to access the request_xml methods and other account info
        account_data = dict()
        account_data['client'] = self

        for param in account_tree.find('CardData'):
            name = param.attrib['name']
            account_data[name] = param.text

        for summary_element in account_tree.find('AccountSummaryData'):
            key = 'value' if 'value' in summary_element.attrib else 'formattedValue'
            name = summary_element.attrib['name']
            account_data[name] = summary_element.attrib[key]

        # Extract the loyalty programmes from the XML
        for element in account_tree.findall('LoyaltyData/RewardsData/param'):
            name = element.attrib['label']
            value = element.attrib['formattedValue'].replace(',', '')
            loyalty_programme = LoyaltyProgramme(name, value)
            self.loyalty_programmes.append(loyalty_programme)

        return CardAccount(account_data)

    def transactions_request_xml(self, card_index, billing_period=0, transaction_type='recent'):
        """
        Generates the XML requests for account transactions

        Parameters
        ----------
        card_index : integer
            The card on account which the request is being generated for

        billing_period : integer
            Which billing period to inspect (0 = most recent)

        transaction_type : str
            Switch between pending or recent transactions
        """
        xml_filename = 'data/statement_request.xml'
        if transaction_type == 'pending':
            xml_filename = 'data/pending_transactions_request.xml'

        xml_filename = pkg_resources.resource_filename(__name__, xml_filename)
        with open(xml_filename, 'r') as xml_file:
            xml = xml_file.read()
            xml = xml.format(locale=self.locale,
                             security_token=self.security_token,
                             card_index=card_index,
                             billing_period=billing_period)

        return xml

    def payments_request_xml(self):
        xml_filename = 'data/recent_payments_request.xml'
        xml_filename = pkg_resources.resource_filename(__name__, xml_filename)
        with open(xml_filename, 'r') as xml_file:
            xml = xml_file.read()

        return xml

    def payments(self):
        """
        Queries the API for all of the card accounts for the user

        Returns : list of CardAccounts

        """
        # get the summary data
        options = {
            'PayLoadText': self.payments_request_xml()
        }

        response = request.get(self.url, params=options) \
            .text
        print(response)

    def request_xml(self):
        """
        Generates the XML to send in a request to fetch cards for
        an account.
        """
        xml_filename = pkg_resources.resource_filename(__name__, 'data/request.xml')
        with open(xml_filename, 'r') as xml_file:
            xml = xml_file.read()
            xml = xml.format(username=self.username,
                             password=self.password,
                             timestamp=time.time(),
                             hardware_id=self.generate_hardware_id(),
                             advertisement_id=self.generate_advertisement_id(),
                             locale=self.locale)
        return xml

    def generate_hardware_id(self):
        """
        Generates a HardwareId to be sent in requests
        """
        return uuid.uuid4()

    def generate_advertisement_id(self):
        """
        Generates an AdvertisementId to be sent in requests
        """
        return uuid.uuid4()
