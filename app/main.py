import streamlit as st
import src.detailed_costs as detailed_costs
import src.monthly_payments as monthly_payments


def main():
    st.title('Mortgage Modeler')
    modes = ["Start", "Detailed Costs", "Compare Payments"]
    mode = st.sidebar.selectbox("Select Mode", modes)
    data = dict()

    if mode == "Start":
        st.subheader("Print some info about app usage")

    elif mode == "Detailed Costs":
        st.sidebar.subheader("Buy Home")
        data = detailed_costs.buy_input(data)
        data = detailed_costs.total_payment(data)
        detailed_costs.buy_output(data)

        st.sidebar.subheader('Sell Home')
        data = detailed_costs.sell_input(data)
        data = detailed_costs.sell_cost(data)
        detailed_costs.sell_output(data)

        data = detailed_costs.comparison(data)
        detailed_costs.compare_output(data)

    elif mode == "Compare Payments":
        st.sidebar.subheader("Compare Monthly Payments")
        data = monthly_payments.buy_input(data)
        data = monthly_payments.model_payments(data)
        monthly_payments.model_output(data)


if __name__ == '__main__':
    main()
