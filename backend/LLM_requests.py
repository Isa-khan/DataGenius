from flask import Flask, render_template, request, redirect, url_for
import os
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
from pyspark.sql import SQLContext
from pyspark import SparkContext


# OpenAI API Key
os.environ['OPENAI_API_KEY'] = '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'

prompt = """You are an AI assistant that must read a csv and answer questions about it, 
any question that I will say after this sentence is the one you must answer, and if at any 
point you are asked something that is not related to the csv or you do not understand, you 
can simply reply with  "Sorry, I am unable to fulfill that request". Here is the question: 
"""

def pre_processing(csv):
    final_cols = []
    removed_cols = []
    for i in csv.columns:
        if i:
            final_cols.append(i)
        else:
            removed_cols.append(i)
    return final_cols

def data_clean(csv):
    pass

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

