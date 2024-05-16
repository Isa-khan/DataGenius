from flask import Flask, render_template, request, redirect, url_for
from langchain_community.llms import OpenAI
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

# OpenAI API Key
os.environ['OPENAI_API_KEY'] = ''

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

