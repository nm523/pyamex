"""
pyamex demo

Get transactions and print a summary by day of week
"""
import pyamex
import getpass
import calendar
import pandas as pd

login = {
	'username': input('Username: '),
	'password': getpass.getpass('Password: '),
	'locale': 'en_GB'
}

# Select the number of billing periods
periods = input('Billing Periods: ')
periods = int(periods)
periods = list(range(0, periods))

client = pyamex.AmexClient(**login)

accounts = client.accounts()

result = []
for account in accounts:
	billing_periods = account.transactions(periods)
	for _, transactions in billing_periods.items():
		for transaction in transactions:
			result.append(
					(account.card_product,
					 account.lending_type,
					 account.card_number_suffix,
					 transaction.date, 
					 transaction.narrative,
					 transaction.trans_amount)
				)

df = pd.DataFrame(result)
df.columns = ['CardProduct', 'LendingType',
              'CardSuffix', 'Date',
              'Description', 'Amount']

df['DayOfWeek'] = df.Date \
                    .map(lambda date : date.weekday())

summary = df[(df.Amount > 0)].groupby('DayOfWeek') \
                             .agg(['mean', 'std', 'min', 'max'])

# Human readable + sorted
summary.index = summary.index.map(lambda day : calendar.day_name[day])
print(summary)
