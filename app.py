import streamlit as st
from streamlit_extras import add_vertical_space

import pandas as pd

import json
import plotly.express as px
import plotly.graph_objs as go

from src.Predictive_Maintenance.pipelines.prediction_pipeline import prediction

with st.sidebar:
    st.title("Predictive Maintenance Project")
    
    choice = st.radio("Choose from the below options:", ["Main","EDA","Monitoring Reports","Performance Measures","Prediction"])
    
   



if choice == "Main":
    with open("README.md", "r") as file:
        readme_contents = file.read()
    st.markdown(readme_contents)
    
    
    
if choice == "EDA":
    st.title('Exploratory Data Analysis')
    
    st.header('Question 1')
    st.write("What is the distribution of the 'machine failure' label in the dataset? How many instances have failed and how many have not failed?")
    
    
    
if choice == "Prediction":
    
    st.title('Predictive Maintenance')
    st.write("**Please enter the following parameters**")
    
    type = st.selectbox(
    'Type',('Low', 'Medium', 'High'))

    st.write('You selected:', type)
    
    rpm = st.number_input('RPM')
    st.write('The current rpm is ', rpm)
    
    torque = st.number_input('Torque')
    st.write('The current rpm is ', torque)
    
    tool_wear = st.number_input('Tool Wear')
    st.write('The current rpm is ', tool_wear)
    
    air_temp = st.number_input('Air Temperature')
    st.write('The current rpm is ', air_temp)
    
    process_temp = st.number_input('Process Temperature')
    st.write('The current rpm is ', process_temp)
    
    if st.button("Predict"):
        
        result1, result2 = prediction(type, rpm, torque, tool_wear, air_temp, process_temp)
    
        st.write("Machine Failure?: ", result1)
        st.write("Type of Failure: ", result2)
        










#type, rpm, torque, tool_wear, air_temp, process_temp