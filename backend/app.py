#from dependancies import *
from flask import Flask, render_template, request, redirect, url_for
import os
from LLM_requests import process_csv
from langchain_community.llms import OpenAI
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql import Row
from pyspark.sql.functions import col, column, from_json, count, isnan, isnull, when, expr, to_timestamp, to_date, explode, flatten, lit, instr, hour, length, concat_ws, concat
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, ArrayType, MapType, IntegerType, BooleanType
from pyspark.sql.functions import col, when, lit
import json
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
#from langchain.llms import OpenAI
from pyspark.sql import SparkSession
from langchain_experimental.agents import create_spark_dataframe_agent
import requests
import openai
import spark
import pyspark
import os
from langchain_community.llms import OpenAI
from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql import Row
from pyspark.sql.functions import col, column, from_json, count, isnan, isnull, when, expr, to_timestamp, to_date, explode, flatten, lit, instr, hour, length, concat_ws, concat
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, ArrayType, MapType, IntegerType, BooleanType
from pyspark.sql.functions import col, when, lit
import json
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
#from langchain.llms import OpenAI
from pyspark.sql import SparkSession
from langchain_experimental.agents import create_spark_dataframe_agent
import requests
import openai
import spark
import pyspark
import os
from langchain_community.llms import OpenAI
from pyspark.sql import SparkSession



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
