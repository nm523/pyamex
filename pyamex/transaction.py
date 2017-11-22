import datetime
import xml.etree.cElementTree

class Transaction:
    """
    Class containing the transactional data for a given transaction
    in an account.
    """

    def __init__(self, transaction):
        """
        Parameter
        ---------
        transaction : xml.etree.cElementTree.ElementTree
            Transaction XML element from the web query
        """
        charge_date = transaction.find('TransChargeDate').text

        date_format = '%m/%d/%y'
        if charge_date:
            self.date = datetime.datetime.strptime(charge_date, date_format)
        else:
            charge_date = transaction.find('*[@name="chargeDate"]').text
            self.date = datetime.datetime.strptime(charge_date, date_format)

        self.narrative = transaction.find('TransDesc').text

        # These two were in the Ruby code but don't appear to work any more
        #self.description = transaction.find('*[@name="TransDesc"]').text
        #self.reference_number = transaction.find('*[@name="transRefNo"]').text

        self.trans_amount = float(transaction.find('TransAmount').text)

        self.extra_details = dict()
        for detail in transaction.findall('TransExtDetail/ExtDetailElement'):
            name = detail.attrib['name']
            self.extra_details[name] = detail.attrib['formattedValue']

    def is_foreign_transaction(self):
        return 'currencyRate' in self.extra_details

    def __repr__(self):
        repr_ = '<Transaction on {date} for {amount}>'
        return repr_.format(date=self.date.strftime('%Y-%m-%d'),
                            amount=self.trans_amount)