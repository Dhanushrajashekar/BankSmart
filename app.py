from flask import Flask,render_template
from transactions import flag_transaction,df



app = Flask(__name__)

@app.route('/')
def welcome_Page():
    return render_template('index.html')
    

df['risk_flag'] = df.apply(flag_transaction, axis=1)

@app.route('/report')
def final_report():
    counts = df['risk_flag'].value_counts()
    fraud = counts('Fraud')
    sus = counts('Suspecious')
    clean = counts('Clean')
    return render_template('report.html', fraud=fraud, sus=sus, clean=clean)
    
    
   

if __name__ == "__main__":
    app.run()