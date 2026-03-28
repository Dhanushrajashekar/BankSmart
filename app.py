from flask import Flask,render_template,request
from transactions import flag_transaction
import pandas as pd
import os
import sqlite3
from datetime import date as dt


def save_to_db(filename, date, fraud, suspicious, clean):
    conn = sqlite3.connect('database.db')    # Create a cursor object to execute SQL statements
    cur = conn.cursor()
    cur.execute('''INSERT into BankSmart(fileName, date, fraud, suspicious, clean) Values(?,?,?,?,?)''',(filename,str(dt.today()), fraud, suspicious, clean))
    conn.commit()
    conn.close()

    


print("RUNNING FROM:", os.path.abspath(__file__))
app = Flask(__name__)


@app.route('/')
def welcome_Page():
    return render_template('index.html')

#Uploading files here 
@app.route('/uploads', methods=['POST'])
def file_upload():
        
    if 'files' not in request.files:
        return "File not present"
    present_file = request.files['files']
    save_Path = ('uploads/' + present_file.filename)
    present_file.save(save_Path)

    new_df = pd.read_csv(save_Path)
    new_df['risk_flag'] = new_df.apply(flag_transaction, axis=1)

    today = dt.today()
    counts = new_df['risk_flag'].value_counts()
    fraud = counts['Fraud']
    sus = counts['Suspecious']
    clean = counts['Clean']
    save_to_db(present_file.filename, str(today) , int(fraud), int(sus), int(clean))
    return render_template('report.html', fraud=fraud, sus=sus, clean=clean)
    

 
   
if __name__ == "__main__":
    app.run(debug=True)