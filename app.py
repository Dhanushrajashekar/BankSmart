from flask import Flask, render_template, request
from transactions import flag_transaction  # the function that decides if a row is fraud/suspicious/clean
import pandas as pd
import os
import sqlite3
from datetime import date as dt


def init_db():
    # run this once at startup so the table exists before anyone tries to insert into it
    # SQLite creates the file automatically but not the tables — learned that the hard way
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS BankSmart (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        fileName  TEXT,
        date      TEXT,
        fraud     INTEGER,
        suspicious INTEGER,
        clean     INTEGER
    )''')
    conn.commit()
    conn.close()


def save_to_db(filename, date, fraud, suspicious, clean):
    # saves the summary counts for each uploaded file so we have a history of past reports
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # using ? placeholders here to avoid SQL injection from filenames
    cur.execute(
        '''INSERT INTO BankSmart(fileName, date, fraud, suspicious, clean) VALUES(?,?,?,?,?)''',
        (filename, str(dt.today()), fraud, suspicious, clean)
    )
    conn.commit()
    conn.close()


print("RUNNING FROM:", os.path.abspath(__file__))
app = Flask(__name__)
init_db()  # make sure the DB table is ready before the first request comes in


@app.route('/')
def welcome_Page():
    return render_template('index.html')


# accepts the CSV the user uploads and runs the fraud analysis on it
@app.route('/uploads', methods=['POST'])
def file_upload():

    if 'files' not in request.files:
        return "File not present"

    present_file = request.files['files']
    save_Path = ('uploads/' + present_file.filename)
    present_file.save(save_Path)  # save it locally so pandas can read it from disk

    # run flag_transaction on every row — adds a 'risk_flag' column to the dataframe
    new_df = pd.read_csv(save_Path)
    new_df['risk_flag'] = new_df.apply(flag_transaction, axis=1)

    today = dt.today()
    counts = new_df['risk_flag'].value_counts()

    # pull out each category count — these go to both the DB and the report page
    fraud = counts['Fraud']
    sus = counts['Suspecious']  # note: typo is intentional to match the value in flag_transaction
    clean = counts['Clean']

    save_to_db(present_file.filename, str(today), int(fraud), int(sus), int(clean))
    return render_template('report.html', fraud=fraud, sus=sus, clean=clean)


if __name__ == "__main__":
    app.run(debug=True)
