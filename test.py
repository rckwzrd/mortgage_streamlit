import streamlit as st
import numpy as np
import pandas as pd

st.title("Mortgage Modeler")

# Buying House Section
# Calculate monthly mortgage payment
st.subheader('Calculate monthly mortgage payment')

mortgage_loan = st.number_input('Loan:', value=300000, format='%.2f')
mortgage_rate = st.number_input('Rate:', value=0.0325, step=0.0001, format='%.4f')
mortgage_term = int(st.number_input('Term:', value=30, format='%i') * 12)

mortgage_rate_periodic = (1+mortgage_rate)**(1/12) - 1
periodic_mortgage_payment = -1*np.pmt(mortgage_rate_periodic, mortgage_term, mortgage_loan)

st.text(f"Monthly mortgage rate: {mortgage_rate_periodic:.4f}, Monthly mortgage payment: {periodic_mortgage_payment:.2f}")

# Estimate Escrow
st.subheader('Estimate escrow')
tax = st.number_input('Yearly Tax:', format='%.2f') / 12
hoa = st.number_input('Monthly HOA:', format='%.2f') 
home_insurance = st.number_input('Yearly Home Insurance:', format='%.2f') / 12

st.text(f"Tax: {tax:.2f}, HOA: {hoa:.2f}, Home Insurance: {home_insurance:.2f}")

# Estimate total monthly payment
total_monthly_payment = periodic_mortgage_payment + hoa + tax + home_insurance
st.text(f"Total Monthly Payment: {total_monthly_payment:.2f}")

# Mortgage and interest payments over time
st.subheader('Mortgage and interest payments over time')
interest_paid = np.zeros((mortgage_term,1))
principal_paid = np.zeros((mortgage_term,1))
principal_remaining = np.zeros([mortgage_term])

for i in range(0, mortgage_term):
    if i == 0:
        previous_principal_remaining = mortgage_loan
    else:
        previous_principal_remaining = principal_remaining[i-1]
    
    interest_payment = round(previous_principal_remaining * mortgage_rate_periodic, 2)
    principal_payment = round(periodic_mortgage_payment - interest_payment, 2)
    
    if previous_principal_remaining - principal_payment < 0:
        principal_payment = previous_principal_remaining
    
    interest_paid[i] = interest_payment
    principal_paid[i] = principal_payment
    principal_remaining[i] = previous_principal_remaining-principal_payment

data = np.hstack((interest_paid,principal_paid))
data = pd.DataFrame(data, columns=['Interest Paid', 'Principal Paid'])

st.line_chart(data)

# TODO: set default and min values, cache input, plot something, add tab for buy and sell


# Selling house sections
# st.subheader("Closing cost estimate")
# closing_cost_percent = st.number_input('Closing Cost %:', 0.03)
# earnest_percent = st.number_input('Closing Cost %:', 0.01)

# # find a place for this
# current_monthly_payment = 2500

# st.text(f"Closing cost: {mortgage_loan*closing_cost_percent:.2f}, Earnest Money: {mortgage_loan*earnest_percent:.2f}")



