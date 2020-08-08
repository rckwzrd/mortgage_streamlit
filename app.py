# TODO:
# make persistent data dict --> declare dict for each tab, merge into main data dict, pass that around
# make comparison --> need persistent dict
# make environment and requirements.txt, git ignore .env --> done
# deploy to server 

import streamlit as st
import SessionState
import numpy as np
import pandas as pd

def main():
    st.sidebar.title('Mortgage Modeler')
    mode = st.sidebar.selectbox('Select Mode', ['Buy','Sell','Compare','Summary','Introduction'])
    state = SessionState.get(data=dict())
    # data = dict() # will this be persistent? --> it is not persistent

    if mode == 'Buy':
        st.title("Buy Home")
        state.data = buy_input(state.data)
        state.data = total_payment(state.data)
        buy_output(state.data)
        st.write(state.data)
    
    elif mode == 'Sell':
        st.title('Sell Home')
        data = sell_input(data)
        data = sell_cost(data)
        sell_output(data)
        st.write(data)
    elif mode == 'Compare':
        st.text('Implement Compare') 
    elif mode == 'Summary':
        st.text('Implement Summary')
    elif mode == 'Introduction':
        st.text('Implement Intro') 

# @st.cache(persist=True, allow_output_mutation=True, suppress_st_warning=True)
def buy_input(data:dict):
    state.data['home'] = st.sidebar.number_input('Home Value:', value=270000.0, step=10000.0, format='%.2f')
    state.data['down'] = st.sidebar.number_input('Downpayment:', value=0.0, step=5000.0, format='%.2f')
    state.data['loan'] = st.sidebar.number_input('Loan Amount:', value=(data['home']-data['down']), step=10000.0, format='%.2f')
    state.data['rate'] = st.sidebar.number_input('Interest Rate:', value=0.0325, step=0.0005, format='%.4f')
    state.data['tax'] = st.sidebar.number_input('Yearly Tax:',value=6000.0, step=250.0, format='%.2f') / 12
    state.data['hoa'] = st.sidebar.number_input('Monthly HOA:', value=0.0, step=50.0, format='%.2f') 
    state.data['insurance'] = st.sidebar.number_input('Yearly Home Insurance:', value=1000.0, step=250.0, format='%.2f') / 12    
    return state.data

# @st.cache(persist=True, allow_output_mutation=True, suppress_st_warning=True)
def total_payment(data:dict):
    state.data['term'] = int(30 * 12)
    state.data['rate_periodic'] = (1+data['rate'])**(1/12) - 1
    state.data['periodic_payment'] = -1*np.pmt(data['rate_periodic'], data['term'], data['loan'])
    state.data['total_payment'] = data['periodic_payment'] + data['hoa'] + data['tax'] + data['insurance']
    return state.data 

def buy_output(data:dict):
    st.subheader(f"Estimated monthly mortgage : ${data['periodic_payment']:.2f}")
    st.text(f"Monthly mortgage rate: {data['rate_periodic']:.4f}%")
    st.subheader(f"Estimated monthly escrow: ${data['hoa'] + data['tax'] + data['insurance']:.2f}")
    st.text(f"Tax: ${data['tax']:.2f}, HOA: ${data['hoa']:.2f}, Home Insurance: ${data['insurance']:.2f}")
    st.subheader(f"Total monthly payment: ${data['total_payment']:.2f}")
    st.text(f"Percent Down: {data['down']:.2f}%, {int(data['term']/12)} year term")

def sell_input(data:dict):
    data['price'] = st.sidebar.number_input('Home Value:', value=360000.0, step=5000.0, format='%.2f')
    data['remainder'] = st.sidebar.number_input('Mortgage Remainder:', value=320000.0, step=5000.0, format='%.2f')
    data['repairs'] = st.sidebar.number_input('Repair Cost:', value=2500.0, step=250.0, format='%.2f') 
    data['title'] = st.sidebar.number_input('Title Cost:', value=1000.0, step=250.0, format='%.2f')
    return data

def sell_cost(data:dict):
    data['profit'] = data['price'] - data['remainder']
    data['commission'] = 0.06 * data['price']
    data['extra_cost'] = data['title'] + data['repairs']
    data['total_cost'] = data['commission'] + data['extra_cost']
    data['net_profit'] = data['profit'] - data['total_cost']
    return data

def sell_output(data:dict):
    st.subheader(f"Estimated cost to sell: ${data['total_cost']:.2f}")
    st.text(f"Realtor commission at 6%: ${data['commission']:.2f}, Title and Repairs: ${data['extra_cost']:.2f}")
    st.subheader(f"Estimated net profit after sale: ${data['net_profit']:.2f}")
    st.text(f"Sale Price: ${data['price']:.2f}, Profit: ${data['profit']:.2f}") 

def compare_input(data:dict):
    pass

def comparison(data:dict):
    pass

def compare_output(data:dict):
    pass

if __name__ == '__main__':
    main()