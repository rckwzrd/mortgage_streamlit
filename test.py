import streamlit as st

st.title("Mortgage Modeler")

st.text("Mortgage inputs:")
loan = st.number_input('Mortgage Loan:')
rate = st.number_input('Mortgage Rate:')
term = st.number_input('Mortgage Term:')

mortgage_loan = 400000.0
mortgage_rate = 0.0325
mortgage_term = 30 * 12

st.text("Upfront cost inputs:")
closing_cost_percent = st.number_input('Closing Cost %:', 0.025 )

closing_cost_percent = 0.025
earnest_percent = 0.01
current_monthly_payment = 2500

st.text(f"Closing Cost: {mortgage_loan*closing_cost_percent:.2f}, Earnest Money: {mortgage_loan*earnest_percent:.2f}")