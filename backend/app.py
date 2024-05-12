from flask import Flask, render_template, request, redirect, url_for
import os
#from LLM_requests import process_csv
from langchain_community.llms import OpenAI
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

os.environ['OPENAI_API_KEY'] = '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'

prompt = """You are an AI assistant that must read a csv and answer questions about it, 
any question that I will say after this sentence is the one you must answer, and if at any 
point you are asked something that is not related to the csv or you do not understand, you 
can simply reply with  "Sorry, I am unable to fulfill that request". Here is the question: 
"""

def process_csv(df, query):
    # Your processing code here
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    result = agent.run(prompt+query)

    return result 

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
