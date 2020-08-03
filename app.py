# TODO: add tab for buy and sell, make tab specific functions, test persistent data dict

# tabs: buy, sell, compare 

# plots go to long term mortgage modeler

import streamlit as st
import numpy as np
import pandas as pd

def main():
    st.sidebar.title('Mortgage Modeler')
    mode = st.sidebar.selectbox('Select Mode', ['Buy','Sell','Compare'])
    data = dict() # will this be persistent? (print it in a table)
    if mode == 'Buy':
        st.title("Buy Home")
        data = buy_input(data)
        data = total_payment(data)
        buy_output(data)
    elif mode == 'Sell':
        st.title('Sell Home')
        data = sell_input(data)
    elif mode == 'Compare':
        st.text('Implement Compare') 
    elif mode == 'Summary':
        st.text('Implement Summary') 

# rename to for buy
def buy_input(data:dict):
    data['home'] = st.number_input('Home Value:', value=270000.0, step=10000.0, format='%.2f')
    data['down'] = st.number_input('Downpayment:', value=0.0, step=5000.0, format='%.2f')
    data['loan'] = st.number_input('Loan Amount:', value=(data['home']-data['down']), step=10000.0, format='%.2f')
    data['rate'] = st.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    data['term'] = int(st.number_input('Term Years:', value=30, format='%i') * 12)
    data['tax'] = st.number_input('Yearly Tax:',value=6000.0, step=250.0, format='%.2f') / 12
    data['hoa'] = st.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    data['insurance'] = st.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12    
    return data

def total_payment(data:dict):
    data['rate_periodic'] = (1+data['rate'])**(1/12) - 1
    data['periodic_payment'] = -1*np.pmt(data['rate_periodic'], data['term'], data['loan'])
    data['total_payment'] = data['periodic_payment'] + data['hoa'] + data['tax'] + data['insurance']
    return data 

def buy_output(data:dict):
    st.subheader('Monthly mortgage estimate:')
    st.text(f"Monthly mortgage payment: ${data['periodic_payment']:.2f}, Monthly mortgage rate: {data['rate_periodic']:.4f}%")
    st.subheader('Monthly escrow estimate:')
    st.text(f"Tax: ${data['tax']:.2f}, HOA: ${data['hoa']:.2f}, Home Insurance: ${data['insurance']:.2f}")
    st.subheader(f"Total monthly payment: ${data['total_payment']:.2f}")
    st.text(f"Percent Down: {data['down']/data['home']:.2f}%")

def sell_input(data:dict):
    data['value'] = st.number_input('Home Value:', value=360000.0, step=5000.0, format='%.2f')
    data['remainder'] = st.number_input('Mortgage Remainder:', value=330000.0, step=5000.0, format='%.2f')
    data['commission'] = st.number_input('Realtor Commision:', value=0.06, step=0.01, format='%.2f')
    data['repairs'] = st.number_input('Repair Cost:', value=2500.0, step=250.0, format='%.2f') 
    data['moving'] = st.number_input('Moving Cost:', value=2500.0, step=250.0, format='%.2f') 
    data['title'] = st.number_input('Title Cost:', value=1000.0, step=250.0, format='%.2f')

def total_cost(data:dict):
    # Estimate total sale profit and cost
    profit = home_price - mortgage_remainder

    realtor_commision = 0.06 * home_price
    additional_cost = moving + title + repairs

    total_cost = realtor_commision + additional_cost

def sell_output(data:dict):
    print(f"Realtor commission: {realtor_commision:.2f}, Additional cost: {additional_cost:.2f}")
    print(f"Profit: {profit:.2f}, Total sale cost: {total_cost:.2f}, Difference: {profit-total_cost:.2f}") 

if __name__ == '__main__':
    main()