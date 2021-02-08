import streamlit as st
import numpy as np


def buy_input(data: dict):
    data['home'] = st.sidebar.number_input('Home Value:', value=270000.0, step=10000.0, format='%.2f')
    data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')

    data['tax'] = st.sidebar.number_input('Yearly Tax:',value=6000.0, step=250.0, format='%.2f') / 12
    data['hoa'] = st.sidebar.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    data['insurance'] = st.sidebar.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12 
    return data


def model_monthly_payments(data: dict):
    house_price = data["home"]
    rate = data["rate"]

    term = float(30 * 12)
    periodic_rate = (1+rate)**(1/12) - 1

    down_payments = np.arange(0.0, 100000, 1000)
    loan_amount = house_price - down_payments
    monthly_payments = np.zeros(down_payments.shape)

    for i in range(len(down_payments)):
        monthly_payments[i] = -1*np.pmt(periodic_rate, term, loan_amount[i])
        print(monthly_payments[i])

    data["down_payments"] = down_payments
    data["monthly_payments"] = monthly_payments

    return data


def plot_payments(data: dict):
    pass
