import streamlit as st
from streamlit_extras import add_vertical_space
import streamlit.components.v1 as components

st.set_page_config(layout='wide')

import pandas as pd

import json
import plotly.express as px
import plotly.graph_objs as go

from src.Predictive_Maintenance.pipelines.prediction_pipeline import prediction

with st.sidebar:
    st.title("Predictive Maintenance Project")
    
    choice = st.radio("Choose from the below options:", ["Main","EDA","Monitoring Reports","Performance Measures","Prediction"])
    
   



if choice == "Main":
    with open("frontend/main/main_page.md", "r") as file:
        readme_contents = file.read()
    st.markdown(readme_contents)
    
    
    
if choice == "EDA":
    st.title('Exploratory Data Analysis')
    
    st.header('Question 1')
    st.write("What is the distribution of the 'machine failure' label in the dataset? How many instances have failed and how many have not failed?")
    
    
    

if choice == "Performance Measures":
    
    pass
    
    
    
    
    
if choice == "Monitoring Reports":
    
    options = st.selectbox('Choose the reports: ',('Data Report', 'Model 1 report', 'Model 2 report'))
    
    if options=='Data Report':
        with open("reports/data_drift.html", "r",encoding="utf-8") as f:
            html_report = f.read()
        
        components.html(html_report, scrolling=True, height=700)
        
        
    if options=='Model 1 report':
        with open("reports/classification_performance_report.html", "r",encoding="utf-8") as f:
            html_report = f.read()
        
        components.html(html_report, height=750, scrolling=True)
        
    if options=='Model 2 report':
        with open("reports/classification_performance_report2.html", "r",encoding="utf-8") as f:
            html_report = f.read()
        
        components.html(html_report, height=750, scrolling=True)
        
    
    
    
    
    

    
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