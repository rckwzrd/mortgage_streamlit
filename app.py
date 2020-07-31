# TODO: annotate and stlye plots, fix equity percent, print out down payment amoutn, add tab for buy and sell

import streamlit as st
import numpy as np
import pandas as pd

def inputs():
    inputs = {}
    inputs['loan'] = st.number_input('Loan Amount:', value=270000, step=10000, format='%.2f')
    inputs['down'] = st.number_input('Downpayment %:', value=0.0, step=0.05, format='%.2f')
    inputs['rate'] = st.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    inputs['term'] = int(st.number_input('Term Years:', value=30, format='%i') * 12)
    inputs['tax'] = st.number_input('Yearly Tax:',value=6000, format='%.2f') / 12
    inputs['hoa'] = st.number_input('Monthly HOA:', value=0, format='%.2f') 
    inputs['insurance'] = st.number_input('Yearly Home Insurance:', value=1000, format='%.2f') / 12    
    return inputs

def total_payment(inputs:dict):
    inputs['rate_periodic'] = (1+inputs['rate'])**(1/12) - 1
    inputs['periodic_payment'] = -1*np.pmt(inputs['rate_periodic'], inputs['term'], inputs['loan'])
    inputs['total_payment'] = inputs['periodic_payment'] + inputs['hoa'] + inputs['tax'] + inputs['insurance']
    return inputs 

def print_output(inputs:dict):
    st.subheader('Monthly mortgage estimate:')
    st.text(f"Monthly mortgage rate: {inputs['rate_periodic']:.4f}, Monthly mortgage payment: {inputs['periodic_payment']:.2f}")
    st.subheader('Monthly escrow estimate:')
    st.text(f"Tax: {inputs['tax']:.2f}, HOA: {inputs['hoa']:.2f}, Home Insurance: {inputs['insurance']:.2f}")
    st.subheader(f"Total monthly payment: {inputs['total_payment']:.2f}")

def interest_vs_principal(inputs:dict):
    st.subheader('Interest vs Principal Over Time')

    interest_paid = np.zeros((inputs['term'],1))
    principal_paid = np.zeros((inputs['term'],1))
    principal_remaining = np.zeros([inputs['term']])

    for i in range(0, inputs['term']):
        # handle the case for the first iteration
        if i == 0:
            previous_principal_remaining = inputs['loan']
        else:
            previous_principal_remaining = principal_remaining[i-1]
        
        interest_payment = round(previous_principal_remaining * inputs['rate_periodic'], 2)
        principal_payment = round(inputs['periodic_payment'] - interest_payment, 2)
        
        # handle case where all principal is paid off in the final period
        if previous_principal_remaining - principal_payment < 0:
            principal_payment = previous_principal_remaining
        
        interest_paid[i] = interest_payment
        principal_paid[i] = principal_payment
        principal_remaining[i] = previous_principal_remaining-principal_payment

    return pd.DataFrame(np.hstack((interest_paid,principal_paid)), columns=['Interest_Paid', 'Principal_Paid'])

def cumulative_equity(data, inputs:dict):
    st.subheader('Cumulative Equity and Interest Over Time')
    down_payment_percent = 0.0
    home_value = ((inputs['loan']) / (1-inputs['down']))

    # calculate the cumulative home equity (principal) over time
    data['Cuml_Home_Equity'] = data['Principal_Paid'].cumsum()

    # calculate the cumulative interest paid over time
    data['Cuml_Interest_Paid'] = data['Interest_Paid'].cumsum()

    # # calculate your percentage home equity over time
    # cumulative_percent_owned = inputs['down'] + (cumulative_home_equity/home_value)

    return data.drop(['Interest_Paid', 'Principal_Paid'], axis=1)

st.title("Mortgage Modeler")
x = inputs()
x = total_payment(x)
print_output(x)
data = interest_vs_principal(x)
st.line_chart(data)
cumulative = cumulative_equity(data, x)
st.line_chart(cumulative)
