import os
import uuid
import time
import urllib.parse
import urllib.request
import xml.etree.cElementTree
from .card import CardAccount
from .loyalty import LoyaltyProgramme

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(FILE_PATH, 'data')

class AmexClient:

    all_urls = {
        'en_GB': {
            'base_uri': 'https://global.americanexpress.com',
            'accounts': '/myca/intl/moblclient/emea/ws.do?Face=en_GB'
        },
        'en_US': {
            'base_uri': 'https://online.americanexpress.com',
            'accounts': '/myca/moblclient/us/v2/ws.do'
        }
    }

    loyalty_programmes = []

    def __init__(self, username, password, locale):
        self.username = username
        self.password = password
        self.locale = locale

        urls = self.all_urls[locale]
        self.url = ''.join([urls['base_uri'], urls['accounts']])

    def accounts(self):
        """
        """
        # create options dictionary of ['body': 'PayLoadText' = request_xml()
        # get the response by posting to the accounts url, passing through
        # the options

        # parse the xml

        # check if there is an error
        # otherwise
        ## get the secruity token
        ## loop through the CardAccounts CardAccount

        # get the summary data
        options = { 'PayLoadText' : self.request_xml() }

        options = urllib.parse.urlencode(options) \
                              .encode()

        response = urllib.request.urlopen(self.url, options) \
                                 .read()

        xml_tree = xml.etree.cElementTree.fromstring(response)

        status = xml_tree.find('ServiceResponse/Status').text
        if status != 'success':
            raise ValueError # TODO: Add better error

        self.security_token = xml_tree.find('ClientSecurityToken').text

        accounts = [ 
                    self.create_account(account)
                    for account in xml_tree.find('CardAccounts') 
                   ]

        return accounts  

    def create_account(self, account_tree):
        # loop through card data params
        # loop through account summary data summary elements

        account_data = dict()
        account_data['client'] = self

        for param in account_tree.find('CardData'):
            name = param.attrib['name']
            account_data[name] = param.text

        for summary_element in account_tree.find('AccountSummaryData'):
            key = 'value' if 'value' in summary_element.attrib else 'formattedValue'
            name = summary_element.attrib['name']
            account_data[name] = summary_element.attrib[key]

        ## append the loyalty schemes to the loyalty_programmes var
        for element in account_tree.findall('LoyaltyData/RewardsData/param'):
            name = element.attrib['label']
            value = element.attrib['formattedValue'].replace(',', '')
            loyalty_programme = LoyaltyProgramme(name, value)
            self.loyalty_programmes.append(loyalty_programme)


        return CardAccount(account_data)


    def transactions_request_xml(self, card_index, \
                                 billing_period=0, transaction_type='recent'):
        """
        """
        # select xml file depending on whether or not the transaction type is pending or recent
        # load the xml file
        # format the local and the security token
        # return the xml
        if transaction_type == 'pending':
            xml_filename = 'pending_transactions_request.xml'
        else:
            xml_filename = 'statement_request.xml'

        xml_filename = os.path.join(DATA_PATH, xml_filename)
        with open(xml_filename, 'r') as xml_file:
            xml = xml_file.read()
            xml = xml.format(locale=self.locale, 
                             security_token=self.security_token,
                             card_index=card_index,
                             billing_period=billing_period)

        return xml

    def request_xml(self):
        """
        Generates the XML to send in a request to fetch cards for
        an account.
        """
        # load XML template
        # formate username, password, timestamp, and locale intro it
        # return the result
        xml_filename = os.path.join(DATA_PATH, 'request.xml')
        with open(xml_filename, 'r') as xml_file:
            xml = xml_file.read()
            xml = xml.format(username=self.username,
                             password=self.password,
                             timestamp=time.time(),
                             hardware_id=self.hardware_id(),
                             advertisement_id=self.advertisement_id(),
                             locale=self.locale)

        return xml

    def hardware_id(self):
        """
        Generates a HardwareId to be sent in requests
        """
        return uuid.uuid4()

    def advertisement_id(self):
        """
        """
        return uuid.uuid4()