from flask import Flask, render_template, request, redirect, url_for
import os
from LLM_requests import process_csv
import pandas as pd

app = Flask(__name__, static_folder='../static', template_folder='templates')  

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html', result="None")

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(filename)

            # Get the query from the form
            query = request.form['query']

            # Pass the DataFrame and query to process_csv function
            result = process_csv(df, query)

            return render_template('analytics.html', result=result)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
