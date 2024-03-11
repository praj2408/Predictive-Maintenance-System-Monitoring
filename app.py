import streamlit as st
from streamlit_extras import add_vertical_space
import streamlit.components.v1 as components
from annotated_text import annotated_text


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
    st.image("reports/q1.png")
    st.write("**The success rate of the mahcine is 96.52% and the highest type of failure is HDF(Heat Dissipation Failure) with 1.15% failure rate**")
    
    
    st.header('Question 2')
    st.write("What is the distribution of the 'productID' variable in the dataset? How many instances are of low, medium, and high quality varients?")
    st.image("reports/q2.png")
    st.write("**Low quality varient makes up majority of the dataset with 60% of the data, followed by medium quality varient with 30% and high quality varient with 10%**")
    
    
    st.header('Question 3')
    st.write("What is the range of values for the continious variables 'air temperature', 'process temperature', 'rotational speed', 'torque', and 'tool wear'?")
    st.write("Are there any outliers in the dataset?")
    st.image("reports/q3.png")
    st.write("**Rotational speed may or may not be actual outliers, therefore we'll keep them in the dataset for now.**")
    
    
    st.header('Question 4')
    st.write("Is there any correlation between the continuous variables and the 'machine failure' label? For example, does the tool wear increase the likelihood of machine failure?")
    st.image("reports/q4.png")
    st.write("**Null Hypothesis: There is no significant relationship between the different colums and Machine Failure**")
    st.write("**Alternate Hypothesis: There is a significant relationship between the tool wear and the machine failure label**")
    st.image("reports/h0.png")


    st.header('Question 5')
    st.write("Is there any correlation between the categorical variable 'productID' and the continuous variable? For example, is the 'rotational speed' higher for high-quality products than for low-quality products? ")
    st.image("reports/q5.png")
    st.write("**Process Temperature seems to have an effect on high quality varient machines. Therefore we can say that Process Temperature is correlated with machine type.**")



if choice == "Performance Measures":
    
    st.title("Model 1")
    annotated_text(("Best Model 1", "Random Forest Classifier"))
    st.image("reports/model1.png")
    
    
    
    st.title("Model 2")
    annotated_text(("Best Model 1", "Random Forest Classifier"))
    st.image("reports/model2.png")
    
    
    
    
    
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
    
    rpm = st.number_input('RPM', value=1410.0)
    st.write('The current rpm is ', rpm)
    
    torque = st.number_input('Torque', value=65.70)
    st.write('The current rpm is ', torque)
    
    tool_wear = st.number_input('Tool Wear', value=191.00)
    st.write('The current rpm is ', tool_wear)
    
    air_temp = st.number_input('Air Temperature', value=25.75)
    st.write('The current rpm is ', air_temp)
    
    process_temp = st.number_input('Process Temperature', value=35.85)
    st.write('The current rpm is ', process_temp)
    
    if st.button("Predict"):
        
        result1, result2 = prediction(type, rpm, torque, tool_wear, air_temp, process_temp)
    
        st.write("Machine Failure?: ", result1)
        st.write("Type of Failure: ", result2)
        










#type, rpm, torque, tool_wear, air_temp, process_temp