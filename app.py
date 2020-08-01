# TODO: make branch no_plot, print out down payment amount, add tab for buy and sell, find out way to update down, loan, and home

# tabs: buy, sell, compare 

# plots go to long term mortgage modeler

import streamlit as st
import numpy as np
import pandas as pd

def main():
    st.sidebar.title('Mortgage Modeler')
    mode = st.sidebar.selectbox('Select Mode', ['Buy','Sell','Compare'])
    if mode == 'Buy':
        st.title("Buy Home")
        data = dict()
        data = get_input(data)
        data = total_payment(data)
        print_output(data)
    elif mode == 'Sell':
        st.text('Implement Sell')
    elif mode == 'Compare':
        st.text('Implement Compare') 

def get_input(data:dict):
    data['home'] = st.number_input('Home Value:', value=270000, step=10000, format='%.2f')
    data['loan'] = st.number_input('Loan Amount:', value=270000, step=10000, format='%.2f')
    data['down'] = st.number_input('Downpayment:', value=0.0, step=1000.0, format='%.2f')
    data['rate'] = st.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    data['term'] = int(st.number_input('Term Years:', value=30, format='%i') * 12)
    data['tax'] = st.number_input('Yearly Tax:',value=6000, format='%.2f') / 12
    data['hoa'] = st.number_input('Monthly HOA:', value=0, format='%.2f') 
    data['insurance'] = st.number_input('Yearly Home Insurance:', value=1000, format='%.2f') / 12    
    return data

def total_payment(data:dict):
    data['rate_periodic'] = (1+data['rate'])**(1/12) - 1
    data['periodic_payment'] = -1*np.pmt(data['rate_periodic'], data['term'], data['loan'])
    data['total_payment'] = data['periodic_payment'] + data['hoa'] + data['tax'] + data['insurance']
    return data 

def print_output(data:dict):
    st.subheader('Monthly mortgage estimate:')
    st.text(f"Monthly mortgage rate: {data['rate_periodic']:.4f}, Monthly mortgage payment: {data['periodic_payment']:.2f}")
    st.subheader('Monthly escrow estimate:')
    st.text(f"Tax: {data['tax']:.2f}, HOA: {data['hoa']:.2f}, Home Insurance: {data['insurance']:.2f}")
    st.subheader(f"Total monthly payment: {data['total_payment']:.2f}")

if __name__ == '__main__':
    main()

