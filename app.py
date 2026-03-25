from flask import Flask
from transactions import flag_transaction,df



app = Flask(__name__)

@app.route('/')
def welcome_Page():
    return 'Welcome to Bank Smart v1'

df['risk_flag'] = df.apply(flag_transaction, axis=1)

@app.route('/report')
def final_report():
    counts = df['risk_flag'].value_counts()
    fraud = counts['Fraud']
    sus = counts ['Suspecious']
    clean = counts['Clean']
    return f'Fraud : {fraud} \n Suspecious : {sus} \n clean : {clean}'
    
    
   

if __name__ == "__main__":
    app.run()