import streamlit as st
import numpy as np

def buy_input(data: dict):
    data['home'] = st.sidebar.number_input('Home Value:', value=270000.0, step=10000.0, format='%.2f')
    data['down'] = st.sidebar.number_input('Downpayment:', value=0.0, step=5000.0, format='%.2f')
    data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    data['tax'] = st.sidebar.number_input('Yearly Tax:',value=6000.0, step=250.0, format='%.2f') / 12
    data['hoa'] = st.sidebar.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    data['insur'] = st.sidebar.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12 
    
    return data

def total_payment(data: dict):
    data['term'] = int(30 * 12)
    data['rate_periodic'] = (1+data['rate'])**(1/12) - 1
    data['loan'] = data['home']-data['down']
    data['periodic_payment'] = -1*np.pmt(data['rate_periodic'], data['term'], data['loan'])
    data['total_payment'] = data['periodic_payment'] + data['hoa'] + data['tax'] + data['insur']   
    
    return data

def buy_output(data: dict):
    st.subheader(f"Estimated monthly mortgage : ${data['periodic_payment']:.2f}")
    st.text(f"Monthly mortgage rate: {data['rate_periodic']:.4f}%")
    st.subheader(f"Estimated monthly escrow: ${data['hoa'] + data['tax'] + data['insur']:.2f}")
    st.text(f"Tax: ${data['tax']:.2f}, HOA: ${data['hoa']:.2f}, Home Insurance: ${data['insur']:.2f}")
    st.subheader(f"Total monthly payment: ${data['total_payment']:.2f}")
    st.text(f"Percent Down: {(data['down']/data['home']):.2f}%, {int(data['term']/12)} year term")

def sell_input(data: dict):
    data['price'] = st.sidebar.number_input('Home Value:', value=360000.0, step=5000.0, format='%.2f')
    data['current_payment'] = st.sidebar.number_input('Current Mortgage:', value=2300.0, step=100.0, format='%.2f')
    data['remainder'] = st.sidebar.number_input('Mortgage Remainder:', value=320000.0, step=5000.0, format='%.2f')
    data['repairs'] = st.sidebar.number_input('Repair Cost:', value=2500.0, step=250.0, format='%.2f') 
    data['title'] = st.sidebar.number_input('Title Cost:', value=1000.0, step=250.0, format='%.2f')
    
    return data

def sell_cost(data: dict):
    data['profit'] = data['price'] - data['remainder']
    data['commission'] = 0.06 * data['price']
    data['extra_cost'] = data['title'] + data['repairs']
    data['total_cost'] = data['commission'] + data['extra_cost']
    data['net_profit'] = data['profit'] - data['total_cost']
    
    return data

def sell_output(data: dict):
    st.subheader(f"Estimated cost to sell: ${data['total_cost']:.2f}")
    st.text(f"Realtor commission at 6%: ${data['commission']:.2f}, Title and Repairs: ${data['extra_cost']:.2f}")
    st.subheader(f"Estimated net profit after sale: ${data['net_profit']:.2f}")
    st.text(f"Sale Price: ${data['price']:.2f}, Profit: ${data['profit']:.2f}") 

def comparison(data: dict):
    data['difference'] = data['total_payment'] - data['current_payment']
    
    return data

def compare_output(data: dict):
    st.subheader("Compare current and estimated mortgage:")
    st.text(f"Current mortgage: ${data['current_payment']:.2f}")
    st.text(f"Estimated mortgage: ${data['total_payment']:.2f}")
    st.text(f"Difference: ${data['difference']:.2f}")
