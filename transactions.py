import pandas as pd
from datetime import date

# load the full dataset for the standalone analysis below
df = pd.read_csv('dataset.csv')

print('----Bank Transaction Report ----')
print()
print(df)

total_transactions = df['transactions'].sum()
total_amountSpent = df['total_amount'].sum()
print()
print("Total transactions:", total_transactions)
print("Total amount spent:", total_amountSpent)

# quick checks — how many rows have result=0, and how many are very high value
df2 = len(df[df["result"] == 0])
print(df2)
df2 = len(df[df["total_amount"] > 40000])
print(df2)

# pull out confirmed fraud rows (result == 2 means fraud in the dataset)
fraudulent = df[df["result"] == 2]
print("Fraudulent transactions:", len(fraudulent))

print(df["result"].value_counts())

# what percentage of the 3000 accounts were fraudulent
final_percentage = (len(fraudulent) / 3000) * 100
print(f"Percentage of fraud transaction {final_percentage}")


def flag_transaction(row):
    # this function is called row-by-row via df.apply() in app.py
    # the order of checks matters — fraud is caught first, then suspicious, then edge cases

    if row['result'] == 2:
        # dataset marks confirmed fraud with result=2
        return 'Fraud'

    elif row['total_amount'] > 30000 and row['locations'] == 1:
        # large amount from a single location is a red flag — could be a card being maxed out
        return 'Suspecious'

    elif row['total_amount'] == row['limit']:
        # hitting the exact credit limit is unusual behaviour worth noting
        return 'Limit reached'

    else:
        return 'Clean'


# apply the flag to every row and print a summary breakdown
df['risk_flag'] = df.apply(flag_transaction, axis=1)
print(df['risk_flag'].value_counts())


today = date.today()
counts = df['risk_flag'].value_counts()
sus = counts['Suspecious']
fraud = counts['Fraud']
clean = counts['Clean']
limit = counts['Limit reached']

# total accounts that need some kind of action taken
total = fraud + sus + limit


# write a plain-text report to readme.txt for anyone who doesn't want to use the web app
with open('readme.txt', 'w') as f:
    f.write('================================\n')
    f.write('BANKSMART FRAUD REPORT\n')
    f.write(f'Generated: {today}\n')
    f.write('================================\n')
    f.write(f'Total accounts analysed: 3,000\n')
    f.write('Total amount at risk: 59,647,615\n')

    f.write('FRAUD BREAKDOWN:\n')
    f.write(f' Confirmed Fraud:    {fraud}\n')
    f.write(f' Suspicious:          {sus} \n')
    f.write(f' Limit Reached:          {limit}\n')
    f.write(f' Clean:              {clean} \n')

    f.write(f'ACTION REQUIRED: {total} accounts need review\n')
    f.write('================================\n')

    f.close()
