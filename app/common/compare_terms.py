import streamlit as st

import numpy as np
import numpy_financial as npf
import pandas as pd

def buy_input(data: dict):
    h1 = st.sidebar.number_input('Home 1:', value=275000.0, step=10000.0, format='%.2f')
    h2 = st.sidebar.number_input('Home 2:', value=325000.0, step=10000.0, format='%.2f')
    h3 = st.sidebar.number_input('Home 3:', value=350000.0, step=10000.0, format='%.2f')
    data['home'] = [h1, h2, h3]

    data['term'] = st.sidebar.number_input('Term:', value=30, step=5)
    data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    data['tax'] = st.sidebar.number_input('Yearly Tax:', value=6000.0, step=250.0, format='%.2f') / 12
    data['hoa'] = st.sidebar.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    data['insr'] = st.sidebar.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12

    return data


def model_payments(data: dict):
    pass


def highlight(df):
    if df["DOWN_PMT"] == 50000:
        return ['color: blue']*4
    else:
        return ['color: black']*4


def model_output(data):
    pass