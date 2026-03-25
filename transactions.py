import pandas as pd
from datetime import date

df = pd.read_csv('dataset.csv')

print('----Bank Transaction Report ----')
print()
print(df)
total_transactions = df['transactions'].sum()
total_amountSpent = df['total_amount'].sum()
print()
print("Total transactions:", total_transactions)
print("Total amount spent:", total_amountSpent)


        
df2 = len(df[df["result"]== 0])
print(df2)
df2 = len(df[df["total_amount"] > 40000])
print(df2)

# Line 1 - filter fraud rows
fraudulent = df[df["result"] == 2]
print("Fraudulent transactions:", len(fraudulent))


print(df["result"].value_counts())


final_percentage = (len(fraudulent)/3000)*100
print(f"Percentage of fraud transaction {final_percentage}")


def flag_transaction(row):
    if row['result'] == 2:
        return 'Fraud'
    elif row['total_amount'] > 30000 and row['locations'] == 1:
        return 'Suspecious'
    elif row['total_amount'] == row['limit']:
        return 'Limit reached'
    else:
        return 'Clean'
    
    
df['risk_flag'] = df.apply(flag_transaction , axis= 1)
print(df['risk_flag'].value_counts())
    
    


today = date.today()
counts = df['risk_flag'].value_counts()
sus = counts['Suspecious']
fraud = counts['Fraud']
clean = counts['Clean']
limit = counts['Limit reached']


total = fraud + sus + limit



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