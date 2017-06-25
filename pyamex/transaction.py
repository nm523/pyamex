import datetime
import xml.etree.cElementTree

class Transaction:

    def __init__(self, transaction):
        # need to find the param name
        charge_date = transaction.find('TransChargeDate').text

        date_format = '%m/%d/%y'
        if charge_date:
            # print('Using trans_charge_date', trans_charge_date)
            self.date = datetime.datetime.strptime(charge_date, date_format)
        else:
            charge_date = transaction.find('*[@name="chargeDate"]').text
            self.date = datetime.datetime.strptime(charge_date, date_format)

        self.narrative = transaction.find('TransDesc').text
        #self.description = transaction.find('*[@name="TransDesc"]').text
        #self.reference_number = transaction.find('*[@name="transRefNo"]').text

        trans_amount = float(transaction.find('TransAmount').text)

        self.extra_details = dict()

        for detail in transaction.findall('TransExtDetail/ExtDetailElement'):
            name = detail.attrib['name']
            self.extra_details[name] = detail.attrib['formattedValue']

        def is_foreign_transaction(self):
            return 'currencyRate' in self.extra_details