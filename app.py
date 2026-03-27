from flask import Flask,render_template,request
from transactions import flag_transaction,df


import os
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
    return 'File Uploaded Successfully'
    

df['risk_flag'] = df.apply(flag_transaction, axis=1)

#Report Values from transaction.py
@app.route('/report')
def final_report():
    counts = df['risk_flag'].value_counts()
    fraud = counts['Fraud']
    sus = counts['Suspecious']
    clean = counts['Clean']
    return render_template('report.html', fraud=fraud, sus=sus, clean=clean)
    

 
   
if __name__ == "__main__":
    app.run(debug=True)