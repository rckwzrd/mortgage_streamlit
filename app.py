# TODO:
# style main page with markdown
# implement check boxes 
# implement downpayment and interest plots with altair
# deploy to server 
# version 2: long term modeling

# DONE:
# convert to single page with side bar, persistent is not working yet
# make environment and requirements.txt, git ignore .env
# implement comparison, need current mortgage 
# refractor functions to helpers.py 

import streamlit as st
import helper

def main():
    st.title('Mortgage Modeler')
    data = dict() 

    st.sidebar.subheader("Buy Home")
    data = helper.buy_input(data)
    data = helper.total_payment(data)
    helper.buy_output(data)
    
    st.sidebar.subheader('Sell Home')
    data = helper.sell_input(data)
    data = helper.sell_cost(data)
    helper.sell_output(data)

    data = helper.comparison(data)
    helper.compare_output(data)

    st.text('Implement downpayment plot') 
    st.text('Implement rate plot') 

    st.write(data)

if __name__ == '__main__':
    main()